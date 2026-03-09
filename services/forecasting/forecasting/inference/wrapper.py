"""
Production-safe inference wrapper. Returns predictions with model/dataset/feature version,
coverage, reliability note, and degraded flag. No fake forecasts when artifact is missing.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import numpy as np
import torch

from ..models.graph_wavenet import GraphWaveNet
from ..models.dcrnn import DCRNN
from ..registry.loader import load_registry_metadata, validate_artifact

logger = logging.getLogger(__name__)


@dataclass
class InferenceResult:
    prediction: np.ndarray
    horizon_steps: int
    entity_ids: list[str]
    model_name: str
    model_version: str
    dataset_version: str
    feature_version: str
    coverage_note: str
    reliability_note: str
    degraded: bool
    latency_ms: Optional[float] = None


class ForecastInferenceWrapper:
    """
    Load registered artifact, run forward pass, return structured result.
    If artifact missing or invalid, do not return learned predictions; caller should use baseline or unavailable.
    """

    def __init__(
        self,
        artifact_dir: Optional[Path] = None,
        max_latency_ms: Optional[float] = 5000.0,
    ):
        self._artifact_dir = Path(artifact_dir) if artifact_dir else None
        self._max_latency_ms = max_latency_ms
        self._model: Optional[torch.nn.Module] = None
        self._meta: Optional[dict] = None
        self._entity_order: list[str] = []

    def load(self, entity_order: list[str]) -> bool:
        """Load model from registry artifact if valid. Returns True if loaded."""
        if not self._artifact_dir or not self._artifact_dir.exists():
            return False
        ckpt_path = self._artifact_dir / "checkpoint.pt"
        if not ckpt_path.exists():
            return False
        meta = load_registry_metadata(self._artifact_dir)
        if not validate_artifact(meta, entity_order):
            logger.warning("Artifact validation failed for %s", self._artifact_dir)
            return False
        try:
            ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=True)
        except Exception as e:
            logger.warning("Failed to load checkpoint: %s", e)
            return False
        model_family = ckpt.get("model_family", "graph_wavenet")
        num_nodes = ckpt.get("num_nodes", 0)
        input_len = ckpt.get("input_len", 12)
        horizon = ckpt.get("horizon", 8)
        if num_nodes != len(entity_order):
            logger.warning("Artifact num_nodes %s != entity_order %s", num_nodes, len(entity_order))
            return False
        if model_family == "graph_wavenet":
            model = GraphWaveNet(num_nodes=num_nodes, input_len=input_len, horizon=horizon)
        elif model_family == "dcrnn":
            model = DCRNN(num_nodes=num_nodes, input_len=input_len, horizon=horizon)
        else:
            return False
        model.load_state_dict(ckpt["model_state"], strict=True)
        model.eval()
        self._model = model
        self._meta = meta
        self._entity_order = list(entity_order)
        return True

    def predict(
        self,
        x: np.ndarray,
        support: np.ndarray,
        entity_ids: Optional[list[str]] = None,
    ) -> Optional[InferenceResult]:
        """
        Run inference. Returns InferenceResult or None if model not loaded or error.
        x: (input_len, N). support: (N, N).
        """
        if self._model is None or self._meta is None:
            return None
        entity_ids = entity_ids or self._entity_order
        if x.shape[1] != len(entity_ids) or support.shape[0] != len(entity_ids):
            return None
        t0 = time.perf_counter()
        try:
            with torch.no_grad():
                x_t = torch.from_numpy(x.astype(np.float32)).unsqueeze(0)
                s_t = torch.from_numpy(support.astype(np.float32))
                pred = self._model(x_t, support=s_t)
                out = pred.squeeze(0).numpy()
        except Exception as e:
            logger.warning("Inference failed: %s", e)
            return None
        latency = (time.perf_counter() - t0) * 1000.0
        if self._max_latency_ms and latency > self._max_latency_ms:
            logger.warning("Inference exceeded max latency: %.0f ms", latency)
        return InferenceResult(
            prediction=out,
            horizon_steps=out.shape[0],
            entity_ids=entity_ids,
            model_name=self._meta.get("model_family", "unknown"),
            model_version=self._meta.get("model_version", "unknown"),
            dataset_version=self._meta.get("dataset_version", "unknown"),
            feature_version=self._meta.get("feature_version", "unknown"),
            coverage_note=f"entities={len(entity_ids)}",
            reliability_note="Learned model; no calibrated uncertainty.",
            degraded=False,
            latency_ms=latency,
        )

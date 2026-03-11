"""
Compare models: Graph WaveNet, DCRNN, simple baselines. Same dataset version.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .metrics import compute_metrics, horizon_metrics


def compare_models(
    y_true: np.ndarray,
    predictions: dict[str, np.ndarray],
    mask: np.ndarray | None = None,
    per_horizon: bool = False,
) -> dict[str, Any]:
    """
    predictions: {"graph_wavenet": (T,N,H), "dcrnn": ..., "persistence": ..., "rolling_mean": ...}
    Returns aggregate and per-model metrics; per-horizon if requested.
    """
    results: dict[str, Any] = {"aggregate": {}, "per_model": {}, "per_horizon": {}}
    for name, y_pred in predictions.items():
        if y_pred.shape != y_true.shape:
            continue
        results["per_model"][name] = compute_metrics(y_true, y_pred, mask)
        if per_horizon and y_true.ndim == 3:
            results["per_horizon"][name] = horizon_metrics(y_true, y_pred, mask)
    return results

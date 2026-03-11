"""
Forecast endpoints. Responses distinguish learned model, statistical baseline, deterministic fallback, and unavailable.
"""

import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Query
from forecasting.features.schema import build_feature_schema
from forecasting.pipeline import get_congestion_forecast
from forecasting.task import DEFAULT_TASK_SPEC

router = APIRouter()


def _artifact_dir() -> Path | None:
    p = os.environ.get("FORECAST_ARTIFACT_DIR")
    return Path(p) if p and p.strip() else None


@router.get(
    "/forecast/status",
    summary="Forecasting engine status",
    description="Health and readiness: model loaded, coverage, degraded mode.",
)
def get_forecast_status() -> dict[str, Any]:
    """Return status: active model, coverage, degraded."""
    artifact = _artifact_dir()
    loaded = artifact and (artifact / "checkpoint.pt").exists() if artifact else False
    return {
        "forecasting_engine": "iridium",
        "model_loaded": loaded,
        "degraded": not loaded,
        "note": "Deterministic baseline active when no artifact loaded.",
    }


@router.get(
    "/forecast/models",
    summary="Registered models",
    description="Model family, version, maturity. No artifact content.",
)
def get_forecast_models() -> dict[str, Any]:
    """List model metadata from registry when artifact dir is set."""
    artifact = _artifact_dir()
    if not artifact or not artifact.exists():
        return {"models": [], "note": "No artifact dir configured (FORECAST_ARTIFACT_DIR)."}
    reg_path = artifact / "registry_metadata.json"
    meta_path = artifact / "training_metadata.json"
    meta = None
    if reg_path.exists():
        import json

        with open(reg_path) as f:
            meta = json.load(f)
    elif meta_path.exists():
        import json

        with open(meta_path) as f:
            data = json.load(f)
            meta = {
                "model_family": data.get("model_family", "unknown"),
                "model_version": "v1",
                "maturity": "candidate",
            }
    if meta:
        return {"models": [meta], "note": "Single artifact dir; one active model."}
    return {"models": [], "note": "No registry or training metadata found."}


@router.get(
    "/forecast/coverage",
    summary="Data coverage",
    description="Entity count, task horizon, and coverage requirements.",
)
def get_forecast_coverage() -> dict[str, Any]:
    """Coverage info from task spec and twin (when available)."""
    spec = DEFAULT_TASK_SPEC
    return {
        "horizon_minutes": spec.horizon_minutes,
        "horizon_steps": spec.horizon_steps,
        "input_window_steps": spec.input_window_steps,
        "min_coverage_ratio": spec.min_coverage_ratio,
        "granularity": spec.granularity.value,
    }


@router.get(
    "/forecast/features",
    summary="Feature schema",
    description="Versioned feature names and schema for training and inference.",
)
def get_forecast_features() -> dict[str, Any]:
    """Return active feature schema version and names."""
    schema = build_feature_schema()
    return {
        "schema_version": schema.get("version"),
        "names": schema.get("names", []),
        "compatible": schema.get("compatible", True),
    }


@router.get(
    "/forecast/congestion",
    summary="Congestion forecast",
    description="Short-horizon congestion or speed forecast. Response model_type: deterministic_baseline | statistical_baseline | ml_baseline; fallback_used when learned model unavailable.",
)
def get_congestion(
    horizon_minutes: int = Query(120, ge=1, le=180, description="Forecast horizon in minutes"),
    segment_ids: str | None = Query(
        None, description="Comma-separated segment IDs; omit for default segment"
    ),
):
    """Congestion forecast. Learned model output when artifact and history available; else deterministic baseline or unavailable."""
    seg_list = [s.strip() for s in (segment_ids or "").split(",") if s.strip()] or None
    result = get_congestion_forecast(horizon_minutes=horizon_minutes, segment_ids=seg_list)
    return result.model_dump(mode="json")

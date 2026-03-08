"""
Forecast endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Query

from forecasting.pipeline import get_congestion_forecast

router = APIRouter()


@router.get(
    "/forecast/congestion",
    summary="Congestion forecast",
    description="Short-horizon (2-3 hour) congestion or speed forecast per segment. Baseline: heuristic from current twin state; ST-GNN planned. Response includes data_status.",
)
def get_congestion(
    horizon_minutes: int = Query(120, ge=1, le=180, description="Forecast horizon in minutes"),
    segment_ids: Optional[str] = Query(None, description="Comma-separated segment IDs; omit for default segment"),
):
    """Short-horizon congestion or speed forecast. Baseline: heuristic."""
    seg_list = [s.strip() for s in (segment_ids or "").split(",") if s.strip()] or None
    result = get_congestion_forecast(horizon_minutes=horizon_minutes, segment_ids=seg_list)
    return result.model_dump(mode="json")

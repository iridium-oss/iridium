"""
Forecast API response schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ForecastSegment(BaseModel):
    """Predicted state for one segment at a time step."""

    segment_id: str
    timestamp: datetime
    speed_kmh: Optional[float] = None
    congestion_score: Optional[float] = Field(None, ge=0, le=1)
    occupancy_pct: Optional[float] = Field(None, ge=0, le=100)


class CongestionForecastResponse(BaseModel):
    """Response for GET /api/v1/forecast/congestion."""

    segments: list[ForecastSegment] = Field(default_factory=list)
    horizon_minutes: int = Field(..., ge=1, le=180)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    model_version: Optional[str] = None
    model_type: Optional[str] = Field(
        None,
        description="deterministic_baseline | statistical_baseline | ml_baseline | experimental",
    )
    model_maturity: Optional[str] = Field(
        None,
        description="production_baseline | experimental | inactive",
    )
    source_coverage: Optional[str] = Field(
        None,
        description="Summary of upstream data coverage (e.g. twin_edges, segment_count).",
    )
    confidence_note: Optional[str] = Field(
        None,
        description="Explanation of confidence or uncertainty; baseline has no calibrated uncertainty.",
    )
    fallback_used: bool = Field(
        False,
        description="True if a fallback or degraded path was used.",
    )
    note: Optional[str] = None
    data_status: Optional[str] = Field(
        None,
        description="live | recorded_real_snapshot | unavailable | configuration_required",
    )

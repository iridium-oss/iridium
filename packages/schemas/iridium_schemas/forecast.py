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
    note: Optional[str] = None
    data_status: Optional[str] = Field(
        None,
        description="live | recorded_real_snapshot | unavailable | configuration_required",
    )

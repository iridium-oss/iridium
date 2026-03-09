"""
Mobility equity score schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DistrictScore(BaseModel):
    """District-level equity indicators."""

    district_id: str
    district_name: Optional[str] = None
    avg_travel_time_to_services_min: Optional[float] = Field(None, ge=0)
    pt_accessibility_proxy: Optional[float] = Field(None, ge=0, le=1)
    modal_availability_proxy: Optional[float] = Field(None, ge=0, le=1)
    affordability_proxy: Optional[float] = Field(None, ge=0, le=1)
    composite_score: Optional[float] = Field(None, ge=0, le=1)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None


class MobilityEquityScore(BaseModel):
    """Response for GET /api/v1/equity/score."""

    districts: list[DistrictScore] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = Field(None, description="Assumptions and limitations")
    data_status: Optional[str] = Field(None, description="live, recorded_real_snapshot, unavailable, configuration_required")
    model_type: Optional[str] = Field(
        None,
        description="deterministic_baseline | rule_baseline",
    )
    model_maturity: Optional[str] = Field(
        None,
        description="production_baseline | experimental | inactive",
    )
    source_coverage: Optional[str] = Field(
        None,
        description="Summary of input coverage (e.g. district count, data source).",
    )
    confidence_note: Optional[str] = Field(
        None,
        description="When data is incomplete, confidence is reduced; see note.",
    )

"""
Mobility equity score schemas.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class DistrictScore(BaseModel):
    """District-level equity indicators."""

    district_id: str
    district_name: str | None = None
    avg_travel_time_to_services_min: float | None = Field(None, ge=0)
    pt_accessibility_proxy: float | None = Field(None, ge=0, le=1)
    modal_availability_proxy: float | None = Field(None, ge=0, le=1)
    affordability_proxy: float | None = Field(None, ge=0, le=1)
    composite_score: float | None = Field(None, ge=0, le=1)
    period_start: datetime | None = None
    period_end: datetime | None = None


class MobilityEquityScore(BaseModel):
    """Response for GET /api/v1/equity/score."""

    districts: list[DistrictScore] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    note: str | None = Field(None, description="Assumptions and limitations")
    data_status: str | None = Field(
        None, description="live, recorded_real_snapshot, unavailable, configuration_required"
    )
    model_type: str | None = Field(
        None,
        description="deterministic_baseline | rule_baseline",
    )
    model_maturity: str | None = Field(
        None,
        description="production_baseline | experimental | inactive",
    )
    source_coverage: str | None = Field(
        None,
        description="Summary of input coverage (e.g. district count, data source).",
    )
    confidence_note: str | None = Field(
        None,
        description="When data is incomplete, confidence is reduced; see note.",
    )

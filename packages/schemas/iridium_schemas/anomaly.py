"""
Anomaly detection schemas.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class AnomalyEvent(BaseModel):
    """Single detected anomaly."""

    anomaly_id: str
    type: str = Field(..., description="incident | closure | demand_surge | statistical_anomaly")
    severity: str = Field(..., description="low | medium | high")
    segment_ids: list[str] = Field(default_factory=list)
    zone_id: str | None = None
    detected_at: datetime
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    description: str | None = None
    recommended_response: str | None = None
    confidence: float | None = Field(
        None, ge=0, le=1, description="Detection confidence; rule baseline may omit."
    )
    source_type: str | None = Field(
        None,
        description="official_alert | observed_disruption | inferred_statistical",
    )
    evidence_summary: str | None = Field(
        None, description="Short summary of evidence (e.g. incident flag, occupancy > 85%)."
    )

"""
Anomaly detection schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AnomalyEvent(BaseModel):
    """Single detected anomaly."""

    anomaly_id: str
    type: str = Field(..., description="incident | closure | demand_surge | statistical_anomaly")
    severity: str = Field(..., description="low | medium | high")
    segment_ids: list[str] = Field(default_factory=list)
    zone_id: Optional[str] = None
    detected_at: datetime
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    description: Optional[str] = None
    recommended_response: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Detection confidence; rule baseline may omit.")
    source_type: Optional[str] = Field(
        None,
        description="official_alert | observed_disruption | inferred_statistical",
    )
    evidence_summary: Optional[str] = Field(None, description="Short summary of evidence (e.g. incident flag, occupancy > 85%).")

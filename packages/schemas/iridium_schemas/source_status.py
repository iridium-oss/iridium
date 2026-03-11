"""
Canonical source status and provenance vocabulary for IRIDIUM.

This module defines stable enums and shared metadata models.
It is used across services and the API to ensure truthful, consistent status fields.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SourceFamily(str, Enum):
    official = "official"
    official_website = "official_website"
    public_api = "public_api"
    public_undocumented = "public_undocumented"
    public_web_observed = "public_web_observed"
    public_web_operational_context = "public_web_operational_context"
    licensed_partner = "licensed_partner"
    permission_required = "permission_required"
    configuration_required = "configuration_required"
    unavailable = "unavailable"


class SourceStatus(str, Enum):
    official = "official"
    official_alerts_only = "official_alerts_only"
    official_website = "official_website"
    public_api = "public_api"
    public_undocumented = "public_undocumented"
    public_web_observed = "public_web_observed"
    public_web_operational_context = "public_web_operational_context"
    licensed_partner = "licensed_partner"
    permission_required = "permission_required"
    configuration_required = "configuration_required"
    unavailable = "unavailable"
    stale = "stale"


class ConfidenceLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    unknown = "unknown"


class SourceMetadata(BaseModel):
    """
    Shared metadata attached to any entity derived from an external source.
    """

    source_provider: str = Field(..., description="Provider identifier, for example bakubus_ayna")
    source_family: SourceFamily = Field(..., description="High-level source family")
    source_status: SourceStatus = Field(..., description="Truthful availability and rights status")
    fetched_at: datetime | None = Field(None, description="Fetch time for provider calls")
    observed_at: datetime | None = Field(
        None, description="Observation time for web observed context"
    )
    source_url: str | None = Field(None, description="Public URL when applicable")
    confidence: ConfidenceLevel = Field(
        ConfidenceLevel.unknown, description="Confidence in mapping or parsing"
    )
    validation_note: str | None = Field(None, description="Non-sensitive validation note")


class DataStatus(str, Enum):
    live = "live"
    recorded_real_snapshot = "recorded_real_snapshot"
    unavailable = "unavailable"
    configuration_required = "configuration_required"
    permission_required = "permission_required"
    stale = "stale"


class ProvenanceSummary(BaseModel):
    """
    Provenance summary for a response or snapshot.
    """

    data_status: DataStatus
    sources: list[SourceMetadata] = Field(default_factory=list)
    note: str | None = None

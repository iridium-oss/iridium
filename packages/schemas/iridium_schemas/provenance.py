"""
Data status and provenance: used in API and UI to show real vs unavailable vs configured-required.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Allowed values for data status in responses and UI
DATA_STATUS_LIVE = "live"
DATA_STATUS_RECORDED_REAL = "recorded_real_snapshot"
DATA_STATUS_UNAVAILABLE = "unavailable"
DATA_STATUS_CONFIGURATION_REQUIRED = "configuration_required"
DATA_STATUS_PERMISSION_REQUIRED = "permission_required"
DATA_STATUS_STALE = "stale"

DATA_STATUS_VALUES = [
    DATA_STATUS_LIVE,
    DATA_STATUS_RECORDED_REAL,
    DATA_STATUS_UNAVAILABLE,
    DATA_STATUS_CONFIGURATION_REQUIRED,
    DATA_STATUS_PERMISSION_REQUIRED,
    DATA_STATUS_STALE,
]


class SourceProvenance(BaseModel):
    """Provenance for a data source or snapshot."""

    source_name: str
    status: str = Field(..., description="One of DATA_STATUS_VALUES")
    fetched_at: Optional[datetime] = None
    provider: Optional[str] = None
    confidence: Optional[str] = None  # e.g. high, medium, low
    note: Optional[str] = None  # e.g. "Credentials missing", "Operator feed not yet provided"


class ProviderRegistryEntry(BaseModel):
    """Single provider in the registry (transit, traffic, etc.)."""

    provider_id: str
    name: str
    status: str = Field(..., description="live | permission_required | unavailable | disabled")
    feed_url: Optional[str] = None
    updated_at: Optional[datetime] = None
    note: Optional[str] = None

"""
Moovit partner adapter. Interface and configuration model only.
Credentials can be added later without redesign.
"""

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from iridium_schemas.transit import (
    TransitPartnerRouteResult,
    PredictedArrival,
    Alert,
    SourceFamily,
    SourceStatus,
)

PROVIDER_ID = "moovit_partner"
ENV_MOOVIT_PARTNER_KEY = "MOOVIT_PARTNER_API_KEY"
ENV_IRIDIUM_MOOVIT_KEY = "IRIDIUM_MOOVIT__API_KEY"
ENV_MOOVIT_API_KEY = "MOOVIT_API_KEY"
ENV_MOOVIT_BASE_URL = "MOOVIT_BASE_URL"
ENV_MOOVIT_PARTNER_BASE_URL = "MOOVIT_PARTNER_BASE_URL"
STATUS_AVAILABLE = "available"
STATUS_PARTNER_REQUIRED = "partner_required"


@dataclass
class MoovitConfig:
    """Configuration model for Moovit partner integration."""

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    enabled: bool = False


def get_moovit_config() -> MoovitConfig:
    """Return current Moovit partner configuration. Reads IRIDIUM_* or legacy env."""
    key = os.environ.get(ENV_IRIDIUM_MOOVIT_KEY) or os.environ.get(ENV_MOOVIT_API_KEY) or os.environ.get(ENV_MOOVIT_PARTNER_KEY)
    base_url = os.environ.get(ENV_MOOVIT_PARTNER_BASE_URL) or os.environ.get(ENV_MOOVIT_BASE_URL)
    return MoovitConfig(
        api_key=key,
        base_url=base_url or None,
        enabled=bool(key),
    )


def get_moovit_status() -> str:
    """Return available | partner_required."""
    return STATUS_AVAILABLE if get_moovit_config().enabled else STATUS_PARTNER_REQUIRED


def fetch_moovit_route_alternatives(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
) -> list[TransitPartnerRouteResult]:
    """Placeholder: returns empty list until partner credentials and API are configured."""
    if not get_moovit_config().enabled:
        return []
    observed_at = datetime.now(timezone.utc)
    return [
        TransitPartnerRouteResult(
            result_id=f"{PROVIDER_ID}_placeholder",
            total_duration_seconds=None,
            transfer_count=None,
            route_variants=[],
            schedules_returned=False,
            observed_at=observed_at,
            source_provider=PROVIDER_ID,
            source_family=SourceFamily.LICENSED_API.value,
            source_status=SourceStatus.PARTNER_REQUIRED.value,
            confidence=None,
            validation_note="Moovit partner API not yet integrated; interface only.",
        )
    ]


def fetch_moovit_arrivals(stop_id: str) -> list[PredictedArrival]:
    """Placeholder: returns empty list until partner API is configured."""
    return []


def fetch_moovit_alerts() -> list[Alert]:
    """Placeholder: returns empty list until partner API is configured."""
    return []

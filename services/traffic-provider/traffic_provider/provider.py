"""
Traffic provider: real segment speeds when configured; otherwise configuration_required.
No synthetic traffic in main path.
"""

import os
from datetime import UTC, datetime

from iridium_schemas.provenance import (
    DATA_STATUS_CONFIGURATION_REQUIRED,
    DATA_STATUS_LIVE,
    DATA_STATUS_RECORDED_REAL,
    SourceProvenance,
)


def _has_traffic_credentials() -> bool:
    """True if a traffic provider API key or equivalent is set."""
    return bool(os.environ.get("TRAFFIC_API_KEY") or os.environ.get("TOMTOM_API_KEY"))


def get_traffic_status() -> SourceProvenance:
    """
    Return provenance for traffic layer. Live only when provider is configured and responding.
    Otherwise configuration_required. No fabricated traffic.
    """
    if not _has_traffic_credentials():
        return SourceProvenance(
            source_name="traffic",
            status=DATA_STATUS_CONFIGURATION_REQUIRED,
            fetched_at=datetime.now(UTC),
            provider=None,
            note="Traffic provider credentials not configured. Set TRAFFIC_API_KEY or provider-specific key.",
        )
    # When credentials exist, a real adapter would be called here. Placeholder: still require adapter implementation.
    return SourceProvenance(  # pragma: no cover
        source_name="traffic",
        status=DATA_STATUS_CONFIGURATION_REQUIRED,
        fetched_at=datetime.now(UTC),
        provider=os.environ.get("TRAFFIC_PROVIDER", "tomtom"),
        note="Traffic provider adapter not yet implemented. Configure TRAFFIC_PROVIDER and credentials.",
    )


def get_segment_speeds(
    segment_ids: list[str] | None = None,
) -> tuple[dict[str, float], SourceProvenance]:
    """
    Return segment_id -> speed_kmh and provenance. When provider is not configured or not implemented,
    returns empty dict and provenance with status configuration_required. No synthetic speeds.
    """
    prov = get_traffic_status()
    if prov.status != DATA_STATUS_LIVE and prov.status != DATA_STATUS_RECORDED_REAL:
        return {}, prov
    # Real adapter would fetch and return speeds here.
    return {}, prov  # pragma: no cover

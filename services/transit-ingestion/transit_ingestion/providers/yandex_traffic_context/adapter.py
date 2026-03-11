"""
Yandex traffic context adapter. Road traffic for Baku.
Exposes: web_observed, licensed_api, or unavailable.
"""

import os
from datetime import UTC, datetime

from iridium_schemas.transit import (
    RoadTrafficContext,
    SourceFamily,
    SourceStatus,
)

PROVIDER_ID = "yandex_traffic_context"
STATUS_WEB_OBSERVED = "web_observed"
STATUS_LICENSED_API = "licensed_api"
STATUS_UNAVAILABLE = "unavailable"
ENV_YANDEX_API_KEY = "YANDEX_TRAFFIC_API_KEY"


def get_traffic_context_status() -> str:
    """Return current status: web_observed, licensed_api, or unavailable."""
    if os.environ.get(ENV_YANDEX_API_KEY):
        return STATUS_LICENSED_API
    # Without API key we do not call Yandex; web scraping of traffic layer is not implemented.
    return STATUS_UNAVAILABLE


def fetch_traffic_context(
    bbox: tuple[float, float, float, float] | None = None,
) -> RoadTrafficContext | None:
    """
    Fetch road traffic context for Baku. Returns None if unavailable.
    When licensed API key is set, could call Yandex; currently returns empty context or None.
    """
    status = get_traffic_context_status()
    observed_at = datetime.now(UTC)
    if status == STATUS_UNAVAILABLE:
        return None
    context_id = f"{PROVIDER_ID}_{int(observed_at.timestamp())}"
    if status == STATUS_LICENSED_API:
        # Placeholder: real implementation would call Yandex routing/traffic API.
        return RoadTrafficContext(
            context_id=context_id,
            observed_at=observed_at,
            segments=[],
            source_provider=PROVIDER_ID,
            source_family=SourceFamily.LICENSED_API.value,
            source_status=SourceStatus.LICENSED_PARTNER.value,
            source_url=None,
            confidence="licensed_api_configured",
            validation_note="API key set; traffic data not yet requested from provider.",
        )
    return RoadTrafficContext(
        context_id=context_id,
        observed_at=observed_at,
        segments=[],
        source_provider=PROVIDER_ID,
        source_family=SourceFamily.PUBLIC_WEB.value,
        source_status=SourceStatus.PUBLIC_WEB_OBSERVED.value,
        source_url=None,
        confidence="web_observed",
        validation_note="Web-observed traffic not implemented; status unavailable.",
    )

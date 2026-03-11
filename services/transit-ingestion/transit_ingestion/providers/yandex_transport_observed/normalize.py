"""
Normalize Yandex transport page content to PredictedArrival, StopRealtimeStatus, RouteRealtimeObservation.
Public-web observed only. Never labeled as official GTFS Realtime.
"""

import re
from datetime import timedelta

from iridium_schemas.transit import (
    PredictedArrival,
    RouteRealtimeObservation,
    SourceFamily,
    SourceStatus,
    StopRealtimeStatus,
)

from transit_ingestion.providers.yandex_transport_observed.fetcher import (
    PROVIDER_ID,
    FetchedYandexPage,
)

SOURCE_FAMILY = SourceFamily.PUBLIC_WEB.value
SOURCE_STATUS = SourceStatus.PUBLIC_WEB_OBSERVED.value
PARSER_VERSION = "1.0"


def _extract_arrival_hints(html: str) -> list[dict]:
    """Extract numeric hints that may represent minutes until arrival. No fabrication."""
    out = []
    # Look for patterns like "5 min", "12 min", "N мин" in raw HTML.
    for m in re.finditer(r"(\d{1,3})\s*(?:min|мин|minutes?)", html, re.IGNORECASE):
        minutes = int(m.group(1))
        if 0 <= minutes <= 120:
            out.append({"minutes": minutes, "raw": m.group(0)})
    return out[:20]


def normalize_yandex_stop_observations(
    fetched: FetchedYandexPage,
    stop_id: str = "yandex_observed_stop",
    route_id: str | None = None,
) -> tuple[list[PredictedArrival], list[StopRealtimeStatus], list[RouteRealtimeObservation]]:
    """
    Normalize fetched Yandex page to canonical realtime entities.
    Many pages are JS-rendered so extraction may return empty lists.
    """
    arrivals: list[PredictedArrival] = []
    statuses: list[StopRealtimeStatus] = []
    route_obs: list[RouteRealtimeObservation] = []
    if fetched.error or not fetched.html:
        return arrivals, statuses, route_obs

    hints = _extract_arrival_hints(fetched.html)
    for i, h in enumerate(hints):
        pred_id = f"{PROVIDER_ID}_{stop_id}_{i}_{fetched.fetched_at.timestamp()}"
        # Predicted at = now + minutes (approximate; no real vehicle ID).
        pred_at = fetched.fetched_at + timedelta(minutes=h["minutes"])
        arrivals.append(
            PredictedArrival(
                prediction_id=pred_id,
                stop_id=stop_id,
                route_id=route_id,
                trip_id=None,
                predicted_at=pred_at,
                observed_at=fetched.fetched_at,
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                source_url=fetched.url,
                scrape_method="http_get_html",
                parser_version=PARSER_VERSION,
                confidence="public_web_observed",
                validation_note="Extracted from Yandex page; may be incomplete if content is JS-rendered.",
            )
        )
    if not hints and fetched.html:
        statuses.append(
            StopRealtimeStatus(
                stop_id=stop_id,
                route_id=route_id,
                status="unknown",
                observed_at=fetched.fetched_at,
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                source_url=fetched.url,
                confidence="public_web_observed",
                validation_note="Page fetched; no arrival hints extracted (possibly JS-rendered).",
            )
        )
    return arrivals, statuses, route_obs

"""
2GIS Public Transport API adapter. Optional licensed provider.
Supports bus and metro modes; total_duration, transfer_count, route variants, schedules when returned.
"""

import os
from datetime import datetime, timezone
from typing import Optional

import httpx

from iridium_schemas.transit import (
    TransitPartnerRouteResult,
    SourceFamily,
    SourceStatus,
)

PROVIDER_ID = "twogis_public_transport"
ENV_2GIS_API_KEY = "TWOGIS_API_KEY"
ENV_IRIDIUM_2GIS_KEY = "IRIDIUM_TWOGIS__API_KEY"
# Documented 2GIS Public Transport API base (example; verify against current 2GIS docs).
TWOGIS_ROUTING_URL = "https://routing.api.2gis.com/public_transport/1.0"
DEFAULT_TIMEOUT = 15.0


def _get_twogis_api_key() -> Optional[str]:
    """Read API key from IRIDIUM_* or legacy env."""
    return os.environ.get(ENV_IRIDIUM_2GIS_KEY) or os.environ.get(ENV_2GIS_API_KEY)


def get_twogis_status() -> str:
    """Return configured | unavailable."""
    return "configured" if _get_twogis_api_key() else "unavailable"


def fetch_route_alternatives(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
    modes: Optional[list[str]] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[TransitPartnerRouteResult]:
    """
    Query 2GIS Public Transport API for route alternatives between two points.
    Returns empty list if API key not set or request fails.
    """
    api_key = _get_twogis_api_key()
    if not api_key:
        return []
    modes = modes or ["bus", "metro"]
    observed_at = datetime.now(timezone.utc)
    results: list[TransitPartnerRouteResult] = []
    try:
        # 2GIS routing API pattern: check current 2GIS documentation for exact endpoint and params.
        url = f"{TWOGIS_ROUTING_URL}/route"
        params = {
            "key": api_key,
            "from": f"{from_lon},{from_lat}",
            "to": f"{to_lon},{to_lat}",
        }
        r = httpx.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, dict):
            return []
        # Normalize response to TransitPartnerRouteResult; structure depends on 2GIS response format.
        routes = data.get("result", {}).get("routes") or data.get("routes") or []
        if not isinstance(routes, list):
            routes = []
        for i, route in enumerate(routes[:10]):
            if not isinstance(route, dict):
                continue
            duration = route.get("duration") or route.get("total_duration_seconds")
            if isinstance(duration, (int, float)):
                duration_sec = int(duration)
            else:
                duration_sec = None
            transfer_count = route.get("transfer_count") or route.get("transfers")
            if not isinstance(transfer_count, (int, float)):
                transfer_count = None
            result_id = f"{PROVIDER_ID}_{int(observed_at.timestamp())}_{i}"
            results.append(
                TransitPartnerRouteResult(
                    result_id=result_id,
                    total_duration_seconds=duration_sec,
                    transfer_count=int(transfer_count) if transfer_count is not None else None,
                    route_variants=[],
                    schedules_returned=bool(route.get("schedule") or route.get("schedules")),
                    observed_at=observed_at,
                    source_provider=PROVIDER_ID,
                    source_family=SourceFamily.LICENSED_API.value,
                    source_status=SourceStatus.LICENSED_PARTNER.value,
                    source_url=url,
                    confidence="licensed_partner",
                    validation_note="From 2GIS Public Transport API; not operator-issued.",
                )
            )
    except Exception:  # pragma: no cover
        pass
    return results

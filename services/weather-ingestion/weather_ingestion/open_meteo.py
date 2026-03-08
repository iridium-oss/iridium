"""
Open-Meteo API client. Real data only; no synthetic fallback.
"""

from datetime import datetime, timezone
from typing import Any, Optional

import httpx

from iridium_schemas.events import WeatherSnapshot
from iridium_schemas.provenance import DATA_STATUS_LIVE, DATA_STATUS_UNAVAILABLE, SourceProvenance

# Baku and Quba coordinates
BAKU = {"lat": 40.4093, "lon": 49.8671, "region_id": "baku"}
QUBA = {"lat": 41.3617, "lon": 48.5136, "region_id": "quba"}
DEFAULT_LOCATIONS = [BAKU, QUBA]
OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"


class WeatherResult:
    """Result of weather fetch with provenance."""

    def __init__(
        self,
        snapshots: list[WeatherSnapshot],
        status: str,
        fetched_at: Optional[datetime] = None,
        note: Optional[str] = None,
    ):
        self.snapshots = snapshots
        self.status = status
        self.fetched_at = fetched_at or datetime.now(timezone.utc)
        self.note = note

    def to_provenance(self) -> SourceProvenance:
        return SourceProvenance(
            source_name="open_meteo",
            status=self.status,
            fetched_at=self.fetched_at,
            provider="Open-Meteo",
            note=self.note,
        )


def fetch_weather(
    locations: Optional[list[dict[str, Any]]] = None,
    timeout_seconds: float = 10.0,
) -> WeatherResult:
    """
    Fetch current and short-term forecast from Open-Meteo for Baku and Quba.
    Returns real data with provenance. On failure returns status unavailable and empty snapshots.
    """
    locations = locations or DEFAULT_LOCATIONS
    snapshots: list[WeatherSnapshot] = []
    now = datetime.now(timezone.utc)

    for loc in locations:
        lat = loc.get("lat")
        lon = loc.get("lon")
        region_id = loc.get("region_id", "unknown")
        if lat is None or lon is None:
            continue
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,precipitation,visibility",
            "hourly": "temperature_2m,precipitation",
            "timezone": "UTC",
            "forecast_days": 1,
        }
        try:
            with httpx.Client(timeout=timeout_seconds) as client:
                resp = client.get(OPEN_METEO_BASE, params=params)
                resp.raise_for_status()
                data = resp.json()
        except Exception:
            return WeatherResult(
                snapshots=[],
                status=DATA_STATUS_UNAVAILABLE,
                fetched_at=now,
                note="Open-Meteo request failed",
            )

        current = data.get("current") or {}
        snapshots.append(
            WeatherSnapshot(
                timestamp=now,
                region_id=region_id,
                temp_c=current.get("temperature_2m"),
                precipitation_mm=current.get("precipitation"),
                visibility_km=current.get("visibility"),
                condition=None,
            )
        )

    return WeatherResult(
        snapshots=snapshots,
        status=DATA_STATUS_LIVE,
        fetched_at=now,
        note="Open-Meteo",
    )

"""
Resolve Baku Metro station coordinates via OpenStreetMap Nominatim.
Controlled station-name matching; ambiguous matches flagged for manual review.
No fabricated coordinates. Rate limit 1 req/s for public Nominatim.
"""

import time
from dataclasses import dataclass, field
from typing import Optional

import httpx

from iridium_schemas.transit import TransitStop

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "IRIDIUM-transit-ingestion/0.1 (Baku Metro OSM resolution; no heavy use)"
MIN_INTERVAL = 1.1
DEFAULT_TIMEOUT = 15.0


@dataclass
class OsmResolutionResult:
    """Result of resolving one station against OSM."""

    stop: TransitStop
    confidence: str  # "high", "ambiguous", "none"
    candidates_count: int = 0


@dataclass
class OsmValidationReport:
    """Validation: stations needing manual review (ambiguous or missing)."""

    ambiguous_stop_ids: list[str] = field(default_factory=list)
    unresolved_stop_ids: list[str] = field(default_factory=list)
    resolved_count: int = 0


def _search_nominatim(
    station_name: str,
    timeout: float = DEFAULT_TIMEOUT,
    client: Optional[httpx.Client] = None,
) -> list[dict]:
    """Query Nominatim for station in Baku. Returns list of place dicts (lat, lon, display_name)."""
    q = f"{station_name}, Baku Metro, Baku, Azerbaijan"
    params = {"q": q, "format": "json", "limit": 5}
    headers = {"User-Agent": USER_AGENT}
    try:
        with client or httpx.Client(timeout=timeout) as c:
            r = c.get(NOMINATIM_URL, params=params, headers=headers)
            r.raise_for_status()
            data = r.json()
    except Exception:  # pragma: no cover
        return []
    if not isinstance(data, list):
        return []
    return data


def resolve_station(
    stop: TransitStop,
    timeout: float = DEFAULT_TIMEOUT,
    client: Optional[httpx.Client] = None,
    last_request_time: Optional[list[float]] = None,
) -> OsmResolutionResult:
    """
    Resolve one metro station to coordinates via OSM.
    High: exactly one candidate used. Ambiguous: multiple candidates; first used, flag for review. None: no result.
    """
    lrt = last_request_time if last_request_time is not None else []
    if lrt:
        elapsed = time.monotonic() - lrt[0]
        if elapsed < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - elapsed)
    lrt.clear()
    lrt.append(time.monotonic())

    name = (stop.name or stop.stop_id).strip()
    if not name:
        return OsmResolutionResult(stop=stop, confidence="none", candidates_count=0)

    candidates = _search_nominatim(name, timeout=timeout, client=client)
    if not candidates:
        return OsmResolutionResult(stop=stop, confidence="none", candidates_count=0)

    first = candidates[0]
    lat = first.get("lat")
    lon = first.get("lon")
    if lat is not None and lon is not None:
        try:
            lat_f = float(lat)
            lon_f = float(lon)
        except (TypeError, ValueError):  # pragma: no cover
            return OsmResolutionResult(stop=stop, confidence="none", candidates_count=len(candidates))
    else:
        return OsmResolutionResult(stop=stop, confidence="none", candidates_count=len(candidates))

    confidence = "high" if len(candidates) <= 1 else "ambiguous"
    updated = stop.model_copy(
        update={
            "lat": lat_f,
            "lon": lon_f,
            "osm_match_confidence": confidence,
        }
    )
    return OsmResolutionResult(stop=updated, confidence=confidence, candidates_count=len(candidates))


def resolve_metro_stations(
    stops: list[TransitStop],
    timeout: float = DEFAULT_TIMEOUT,
    rate_limit_interval: float = MIN_INTERVAL,
) -> tuple[list[TransitStop], OsmValidationReport]:
    """
    Resolve all metro stations via OSM. Enforces rate limit between requests.
    Returns (updated stops with coordinates where resolved, validation report for ambiguous/unresolved).
    """
    report = OsmValidationReport()
    last_request_time: list[float] = []
    seen_stop_id: dict[str, TransitStop] = {}
    for s in stops:
        if s.stop_id in seen_stop_id:
            continue
        seen_stop_id[s.stop_id] = s
    unique_stops = list(seen_stop_id.values())
    result_stops: list[TransitStop] = []
    for stop in unique_stops:
        res = resolve_station(stop, timeout=timeout, last_request_time=last_request_time)
        result_stops.append(res.stop)
        if res.confidence == "ambiguous":
            report.ambiguous_stop_ids.append(res.stop.stop_id)
        elif res.confidence == "none":
            report.unresolved_stop_ids.append(res.stop.stop_id)
        else:
            report.resolved_count += 1
    return result_stops, report


def flag_ambiguous_for_manual_review(
    resolution_report: OsmValidationReport,
) -> list[str]:
    """Return stop_ids that should be manually reviewed (ambiguous OSM matches)."""
    return list(resolution_report.ambiguous_stop_ids)

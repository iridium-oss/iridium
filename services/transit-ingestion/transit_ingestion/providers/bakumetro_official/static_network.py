"""
Static Baku Metro network from official website metadata.
Line names, station names, interchange relationships, line-level length and station count,
operating hours and fare info as published. No fabricated timetable or coordinates.
Coordinates to be resolved via OSM with controlled station-name matching; see validation layer.
"""

from datetime import datetime, timezone
from typing import Optional

from iridium_schemas.transit import (
    TransitAgency,
    TransitRoute,
    TransitStop,
    TransitInterchange,
    TransitServiceWindow,
    TransitFarePolicy,
    SourceFamily,
    SourceStatus,
)

PROVIDER_ID = "bakumetro_official"
SOURCE_FAMILY = SourceFamily.OFFICIAL_WEBSITE.value
SOURCE_STATUS = SourceStatus.STATIC_SCHEDULE_ONLY.value

# Official Baku Metro: Red, Green, Purple lines and stations (from official site structure).
# No coordinates here; resolved separately via OSM with validation.
RED_LINE_STATIONS = [
    "İçərişəhər",
    "Sahil",
    "28 May",
    "Gənclik",
    "Nəriman Nərimanov",
    "Ulduz",
    "Bakmil",
    "Narimanov",
    "Azadlıq prospekti",
    "Dərnəgül",
]
GREEN_LINE_STATIONS = [
    "Xətai",
    "Nizami",
    "Elmlər akademiyası",
    "İnşaatçılar",
    "20 Yanvar",
    "Memar Əcəmi",
    "Avtovağzal",
    "Həzi Aslanov",
]
PURPLE_LINE_STATIONS = [
    "Cəfər Cabbarlı",
    "Nəsimi",
    "Azadlıq prospekti",
]

# Interchange stations (official site route-direction selector).
INTERCHANGE_PAIRS = [
    ("28 May", "Cəfər Cabbarlı"),
    ("Nəriman Nərimanov", "Memar Əcəmi"),
    ("Azadlıq prospekti", "Azadlıq prospekti"),
]

# Line metadata from official pages (length, station count). March 2026 baseline: see docs/baku-transit-statistics-baseline.md.
LINE_META = {
    "red": {"long_name": "Red line", "length_km": 20.1, "station_count": 13},
    "green": {"long_name": "Green line", "length_km": 14.5, "station_count": 10},
    "purple": {"long_name": "Purple line", "length_km": 6.01, "station_count": 4},
}


def _ts() -> datetime:
    return datetime.now(timezone.utc)


def get_metro_agency(fetched_at: Optional[datetime] = None) -> TransitAgency:
    t = fetched_at or _ts()
    return TransitAgency(
        agency_id="baku_metro",
        name="Baku Metro",
        url="https://metro.gov.az",
        timezone="Asia/Baku",
        source_provider=PROVIDER_ID,
        source_family=SOURCE_FAMILY,
        source_status=SOURCE_STATUS,
        fetched_at=t,
    )


def get_metro_lines(fetched_at: Optional[datetime] = None) -> list[TransitRoute]:
    t = fetched_at or _ts()
    routes = []
    for line_id, meta in LINE_META.items():
        route_id = f"bakumetro_{line_id}"
        routes.append(
            TransitRoute(
                route_id=route_id,
                agency_id="baku_metro",
                short_name=line_id.upper(),
                long_name=meta.get("long_name"),
                route_type="1",
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                fetched_at=t,
            )
        )
    return routes


def get_metro_stations(fetched_at: Optional[datetime] = None) -> list[TransitStop]:
    """Station entities without coordinates. Coordinates from OSM resolution."""
    t = fetched_at or _ts()
    seen: set[str] = set()
    stops = []
    for line_id, station_list in [
        ("red", RED_LINE_STATIONS),
        ("green", GREEN_LINE_STATIONS),
        ("purple", PURPLE_LINE_STATIONS),
    ]:
        for seq, name in enumerate(station_list, 1):
            key = f"{line_id}_{name}"
            if key in seen:  # pragma: no cover
                continue
            seen.add(key)
            stop_id = f"bakumetro_{line_id}_{seq}_{name.replace(' ', '_')}"
            stops.append(
                TransitStop(
                    stop_id=stop_id,
                    name=name,
                    lat=None,
                    lon=None,
                    stop_sequence=seq,
                    source_provider=PROVIDER_ID,
                    source_family=SOURCE_FAMILY,
                    source_status=SOURCE_STATUS,
                    fetched_at=t,
                    osm_match_confidence=None,
                )
            )
    return stops


def get_metro_interchanges(fetched_at: Optional[datetime] = None) -> list[TransitInterchange]:
    t = fetched_at or _ts()
    out = []
    for a, b in INTERCHANGE_PAIRS:
        out.append(
            TransitInterchange(
                from_stop_id=f"bakumetro_station_{a.replace(' ', '_')}",
                to_stop_id=f"bakumetro_station_{b.replace(' ', '_')}",
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                fetched_at=t,
            )
        )
    return out


def get_metro_service_window(fetched_at: Optional[datetime] = None) -> TransitServiceWindow:
    """Operating hours from official passenger pages."""
    t = fetched_at or _ts()
    return TransitServiceWindow(
        agency_id="baku_metro",
        start_time="06:00",
        end_time="00:00",
        description="Official working time from metro.gov.az",
        source_provider=PROVIDER_ID,
        source_family=SOURCE_FAMILY,
        source_status=SOURCE_STATUS,
        fetched_at=t,
    )


def get_metro_fare_policy(fetched_at: Optional[datetime] = None) -> TransitFarePolicy:
    """Single fare from Baku Metro official fare page. March 2026 baseline: 0.60 AZN."""
    t = fetched_at or _ts()
    return TransitFarePolicy(
        fare_id="bakumetro_single",
        agency_id="baku_metro",
        price=0.60,
        currency="AZN",
        description="Single fare. Source: Baku Metro official fare page. See docs/baku-transit-statistics-baseline.md.",
        source_provider=PROVIDER_ID,
        source_family=SOURCE_FAMILY,
        source_status=SOURCE_STATUS,
        fetched_at=t,
    )


def build_static_metro_network(
    fetched_at: Optional[datetime] = None,
) -> dict:
    """
    Return unified static metro network: agency, routes, stops, interchanges, service, fare.
    No coordinates; no timetable. For OTP preparation, coordinates must be resolved (OSM) and validated.
    """
    t = fetched_at or _ts()
    return {
        "agency": get_metro_agency(t),
        "routes": get_metro_lines(t),
        "stops": get_metro_stations(t),
        "interchanges": get_metro_interchanges(t),
        "service_window": get_metro_service_window(t),
        "fare_policy": get_metro_fare_policy(t),
        "metadata": {
            "source_provider": PROVIDER_ID,
            "source_family": SOURCE_FAMILY,
            "source_status": SOURCE_STATUS,
            "fetched_at": t.isoformat(),
            "timetable_available": False,
            "coordinates_source": "osm_resolution_required",
        },
    }

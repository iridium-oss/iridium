"""
Baku Metro from official website as primary source of truth.
Source: official_website. Status: static_schedule_only (no machine-readable GTFS).
Line names, station names, interchange relationships, line lengths, operating hours, fare info.
Station coordinates resolved via OpenStreetMap with validation; ambiguous matches flagged.
"""

from transit_ingestion.providers.bakumetro_official.osm_resolution import (
    OsmResolutionResult,
    OsmValidationReport,
    flag_ambiguous_for_manual_review,
    resolve_metro_stations,
    resolve_station,
)
from transit_ingestion.providers.bakumetro_official.static_network import (
    build_static_metro_network,
    get_metro_agency,
    get_metro_fare_policy,
    get_metro_interchanges,
    get_metro_lines,
    get_metro_service_window,
    get_metro_stations,
)

__all__ = [
    "get_metro_agency",
    "get_metro_lines",
    "get_metro_stations",
    "get_metro_interchanges",
    "get_metro_service_window",
    "get_metro_fare_policy",
    "build_static_metro_network",
    "resolve_station",
    "resolve_metro_stations",
    "flag_ambiguous_for_manual_review",
    "OsmResolutionResult",
    "OsmValidationReport",
]

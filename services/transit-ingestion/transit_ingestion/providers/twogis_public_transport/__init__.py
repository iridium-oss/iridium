"""
2GIS Public Transport API. Documented developer API for route building, schedule-aware routing, bus/metro.
source_family: licensed_api. source_status: licensed_partner.
Used for route-planning and ETA enrichment; not operator-issued ground truth.
"""

from transit_ingestion.providers.twogis_public_transport.adapter import (
    fetch_route_alternatives,
    get_twogis_status,
)

__all__ = ["get_twogis_status", "fetch_route_alternatives"]

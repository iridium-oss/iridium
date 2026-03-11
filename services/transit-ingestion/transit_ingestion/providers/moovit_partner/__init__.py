"""
Moovit partner adapter. Future-ready; credentials not assumed.
source_family: licensed_api. source_status: partner_required.
"""

from transit_ingestion.providers.moovit_partner.adapter import (
    fetch_moovit_route_alternatives,
    get_moovit_config,
    get_moovit_status,
)

__all__ = ["get_moovit_status", "get_moovit_config", "fetch_moovit_route_alternatives"]

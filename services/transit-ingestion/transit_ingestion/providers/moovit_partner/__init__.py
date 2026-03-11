"""
Moovit partner adapter. Future-ready; credentials not assumed.
source_family: licensed_api. source_status: partner_required.
"""

from transit_ingestion.providers.moovit_partner.adapter import (
    get_moovit_status,
    get_moovit_config,
    fetch_moovit_route_alternatives,
)

__all__ = ["get_moovit_status", "get_moovit_config", "fetch_moovit_route_alternatives"]

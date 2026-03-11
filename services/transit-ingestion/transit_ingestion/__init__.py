"""
Transit data ingestion: GTFS static and Realtime. Provider registry only;
no fabricated feeds. Baku Metro and BakuBus are permission_required until operator provides feed.
"""

from transit_ingestion.registry import ProviderStatus, get_provider_registry

__all__ = ["get_provider_registry", "ProviderStatus"]

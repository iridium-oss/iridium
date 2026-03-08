"""
Unified transit model: merge BakuBus (AYNA) and Baku Metro into one canonical snapshot.
"""

from transit_ingestion.normalization.merge import build_unified_transit_snapshot

__all__ = ["build_unified_transit_snapshot"]

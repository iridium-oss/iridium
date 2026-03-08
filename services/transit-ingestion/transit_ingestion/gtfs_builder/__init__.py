"""
GTFS Static builder from normalized transit data.
Repository-generated; not operator-issued. Only files with defensible data are produced.
"""

from transit_ingestion.gtfs_builder.build import build_gtfs_static, GTFS_BUILD_LABEL

__all__ = ["build_gtfs_static", "GTFS_BUILD_LABEL"]

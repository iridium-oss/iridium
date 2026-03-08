"""
Validation: canonical schema checks, GTFS checks, station-coordinate match flags.
"""

from transit_ingestion.validation.readiness import compute_readiness_report

__all__ = ["compute_readiness_report"]

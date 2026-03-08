"""
Ingestion pipeline: normalise and validate incoming data into shared schemas.
Baseline: file-based and in-memory staging. Future: streaming ingestion.
"""

from ingestion.pipeline import run_ingestion, validate_batch

__all__ = ["run_ingestion", "validate_batch"]

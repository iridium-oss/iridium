"""
Partition manifest schema and strategy enum.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class PartitionStrategy(str, Enum):
    BY_DISTRICT = "by_district"
    BY_PROVIDER = "by_provider"
    BY_SOURCE_FAMILY = "by_source_family"
    BY_TIME_BLOCK = "by_time_block"
    SYNTHETIC_INSTITUTION = "synthetic_institution"  # Simulation only; clearly marked


class PartitionManifest(BaseModel):
    partition_id: str = Field(..., description="Unique partition identifier")
    strategy: PartitionStrategy = Field(...)
    coverage_interval_start: Optional[str] = Field(None, description="ISO datetime or date")
    coverage_interval_end: Optional[str] = None
    source_types: list[str] = Field(default_factory=list, description="e.g. metro, bus, road")
    label_availability: str = Field("full", description="full | partial | none")
    sample_count: int = Field(0, ge=0)
    missingness_pct: Optional[float] = Field(None, ge=0, le=100)
    geography: Optional[str] = Field(None, description="District or region code")
    metadata: dict[str, Any] = Field(default_factory=dict)
    version: str = Field("v1", description="Manifest schema version")

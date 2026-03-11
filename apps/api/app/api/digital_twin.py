"""
Digital twin API.

The digital twin snapshot is assembled from real sources only.
Responses include explicit data_status and provenance.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from digital_twin.state_assembler import get_assembled_snapshot
from fastapi import APIRouter
from iridium_schemas.network import DigitalTwinSnapshot
from pydantic import BaseModel, Field

router = APIRouter()


class DigitalTwinStatusResponse(BaseModel):
    snapshot_at: datetime
    data_status: str
    node_count: int
    edge_count: int
    note: str


class DigitalTwinCoverageResponse(BaseModel):
    snapshot_at: datetime
    data_status: str
    coverage: dict[str, Any] = Field(default_factory=dict)


class DigitalTwinProvenanceResponse(BaseModel):
    snapshot_at: datetime
    data_status: str
    sources: list[dict] = Field(default_factory=list)


@router.get(
    "/digital-twin/snapshot",
    response_model=DigitalTwinSnapshot,
    summary="Digital twin snapshot",
    description="Assembled snapshot including network topology and source provenance. Real sources only.",
)
def get_snapshot() -> DigitalTwinSnapshot:
    return get_assembled_snapshot()


@router.get(
    "/digital-twin/status",
    response_model=DigitalTwinStatusResponse,
    summary="Digital twin status",
    description="High-level status for the assembled digital twin snapshot.",
)
def get_status() -> DigitalTwinStatusResponse:
    snap = get_assembled_snapshot()
    note = "Assembled from configured real sources"
    if snap.data_status != "live":
        note = "Digital twin is incomplete or unavailable. See provenance for details."
    return DigitalTwinStatusResponse(
        snapshot_at=snap.snapshot_at or datetime.now(UTC),
        data_status=snap.data_status,
        node_count=len(snap.nodes),
        edge_count=len(snap.edges),
        note=note,
    )


@router.get(
    "/digital-twin/coverage",
    response_model=DigitalTwinCoverageResponse,
    summary="Digital twin coverage",
    description="Coverage and completeness signals for the digital twin. Does not imply availability of missing sources.",
)
def get_coverage() -> DigitalTwinCoverageResponse:
    snap = get_assembled_snapshot()
    coverage = {
        "network_loaded": len(snap.nodes) > 0 or len(snap.edges) > 0,
        "sources_reported": len(snap.source_provenance or []),
    }
    return DigitalTwinCoverageResponse(
        snapshot_at=snap.snapshot_at or datetime.now(UTC),
        data_status=snap.data_status,
        coverage=coverage,
    )


@router.get(
    "/digital-twin/provenance",
    response_model=DigitalTwinProvenanceResponse,
    summary="Digital twin provenance",
    description="Returns the source provenance list for the assembled snapshot.",
)
def get_provenance() -> DigitalTwinProvenanceResponse:
    snap = get_assembled_snapshot()
    return DigitalTwinProvenanceResponse(
        snapshot_at=snap.snapshot_at or datetime.now(UTC),
        data_status=snap.data_status,
        sources=list(snap.source_provenance or []),
    )

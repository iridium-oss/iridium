"""
Network and digital twin schemas: nodes, edges, snapshot.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class NetworkNode(BaseModel):
    """Single node in the mobility graph (segment, junction, or stop)."""

    node_id: str
    node_type: str = Field(..., description="segment | junction | stop")
    lat: float | None = Field(None, ge=-90, le=90)
    lon: float | None = Field(None, ge=-180, le=180)
    name: str | None = None
    mode: str | None = Field(None, description="bus | metro | minibus | walking | cycling | road")
    metadata: dict = Field(default_factory=dict)


class NetworkEdge(BaseModel):
    """Directed edge between two nodes with optional dynamic state."""

    edge_id: str
    from_node: str
    to_node: str
    mode: str = Field(..., description="bus | metro | minibus | walking | cycling | road")
    length_km: float | None = Field(None, ge=0)
    travel_time_min: float | None = Field(None, ge=0)
    cost: float | None = Field(None, ge=0)
    carbon_kg: float | None = Field(None, ge=0)
    speed_kmh: float | None = Field(None, ge=0)
    occupancy_pct: float | None = Field(None, ge=0, le=100)
    incident: bool = False
    updated_at: datetime | None = None


class DigitalTwinSnapshot(BaseModel):
    """Snapshot of the digital twin: graph, timestamp, and data status."""

    nodes: list[NetworkNode] = Field(default_factory=list)
    edges: list[NetworkEdge] = Field(default_factory=list)
    snapshot_at: datetime | None = None
    version: str | None = None
    data_status: str | None = Field(
        None,
        description="live | recorded_real_snapshot | unavailable | configuration_required | permission_required | stale",
    )
    source_provenance: list[dict] | None = Field(
        None, description="Per-source provenance for UI and API"
    )

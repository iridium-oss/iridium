"""
Network and digital twin schemas: nodes, edges, snapshot.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NetworkNode(BaseModel):
    """Single node in the mobility graph (segment, junction, or stop)."""

    node_id: str
    node_type: str = Field(..., description="segment | junction | stop")
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lon: Optional[float] = Field(None, ge=-180, le=180)
    name: Optional[str] = None
    mode: Optional[str] = Field(None, description="bus | metro | minibus | walking | cycling | road")
    metadata: dict = Field(default_factory=dict)


class NetworkEdge(BaseModel):
    """Directed edge between two nodes with optional dynamic state."""

    edge_id: str
    from_node: str
    to_node: str
    mode: str = Field(..., description="bus | metro | minibus | walking | cycling | road")
    length_km: Optional[float] = Field(None, ge=0)
    travel_time_min: Optional[float] = Field(None, ge=0)
    cost: Optional[float] = Field(None, ge=0)
    carbon_kg: Optional[float] = Field(None, ge=0)
    speed_kmh: Optional[float] = Field(None, ge=0)
    occupancy_pct: Optional[float] = Field(None, ge=0, le=100)
    incident: bool = False
    updated_at: Optional[datetime] = None


class DigitalTwinSnapshot(BaseModel):
    """Snapshot of the digital twin: graph, timestamp, and data status."""

    nodes: list[NetworkNode] = Field(default_factory=list)
    edges: list[NetworkEdge] = Field(default_factory=list)
    snapshot_at: Optional[datetime] = None
    version: Optional[str] = None
    data_status: Optional[str] = Field(
        None,
        description="live | recorded_real_snapshot | unavailable | configuration_required | permission_required | stale",
    )
    source_provenance: Optional[list[dict]] = Field(None, description="Per-source provenance for UI and API")

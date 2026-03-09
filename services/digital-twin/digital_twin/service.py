"""
Digital twin service: in-memory graph and state overlay.
Primary API path should use get_assembled_snapshot (state_assembler) for real-data mode.
This module retains get_graph/update_state/get_snapshot for legacy or test use only when explicitly enabled.
"""

from datetime import datetime, timezone
from typing import Optional

from iridium_schemas.network import (
    DigitalTwinSnapshot,
    NetworkNode,
    NetworkEdge,
)

# In-memory cache when real network is loaded via network-import (optional). Not used for synthetic default in main path.
_nodes: list[NetworkNode] = []
_edges: list[NetworkEdge] = []
_version = "0.2.0"
_snapshot_at: Optional[datetime] = None


def get_graph() -> tuple[list[NetworkNode], list[NetworkEdge]]:
    """Return current nodes and edges. Empty until loaded from PostGIS/network-import."""
    return _nodes, _edges


def set_graph(nodes: list[NetworkNode], edges: list[NetworkEdge]) -> None:
    """Set graph from network-import or DB. Used when real network is loaded."""
    global _nodes, _edges
    _nodes = nodes
    _edges = edges


def update_state(
    segment_speeds: Optional[dict[str, float]] = None,
    segment_occupancy: Optional[dict[str, float]] = None,
    incident_edges: Optional[list[str]] = None,
) -> None:
    """Overlay dynamic state onto edges."""
    global _edges, _snapshot_at
    if segment_speeds:
        for e in _edges:
            e.speed_kmh = segment_speeds.get(e.edge_id)
    if segment_occupancy:
        for e in _edges:
            e.occupancy_pct = segment_occupancy.get(e.edge_id)
    if incident_edges:
        for e in _edges:
            e.incident = e.edge_id in incident_edges
    _snapshot_at = datetime.now(timezone.utc)


def get_snapshot() -> DigitalTwinSnapshot:
    """
    Produce snapshot from in-memory graph. Use get_assembled_snapshot for API to get real-data status and provenance.
    This returns whatever is in memory (may be empty if no real network loaded).
    """
    nodes, edges = get_graph()
    return DigitalTwinSnapshot(
        nodes=nodes,
        edges=edges,
        snapshot_at=_snapshot_at or datetime.now(timezone.utc),
        version=_version,
    )

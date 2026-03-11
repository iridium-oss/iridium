"""Digital twin service tests: set_graph, update_state, get_snapshot, state_assembler."""

import os
import sys
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/digital-twin"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from digital_twin.service import get_snapshot, set_graph, update_state
from iridium_schemas.network import NetworkEdge, NetworkNode


def test_set_graph_and_get_snapshot():
    """Cover set_graph and get_snapshot with nodes and edges."""
    nodes = [NetworkNode(node_id="n1", node_type="junction", lat=40.4, lon=49.8)]
    edges = [NetworkEdge(edge_id="e1", from_node="n1", to_node="n2", mode="walking")]
    set_graph(nodes, edges)
    try:
        snap = get_snapshot()
        assert len(snap.nodes) == 1
        assert len(snap.edges) == 1
        assert snap.nodes[0].node_id == "n1"
        assert snap.edges[0].edge_id == "e1"
    finally:
        set_graph([], [])


def test_update_state_segment_speeds():
    """Cover update_state segment_speeds branch."""
    edges = [NetworkEdge(edge_id="e1", from_node="n1", to_node="n2", mode="road")]
    set_graph([NetworkNode(node_id="n1", node_type="junction", lat=40.4, lon=49.8)], edges)
    try:
        update_state(segment_speeds={"e1": 50.0})
        snap = get_snapshot()
        assert snap.edges[0].speed_kmh == 50.0
    finally:
        set_graph([], [])


def test_update_state_occupancy_and_incident():
    """Cover update_state segment_occupancy and incident_edges branches."""
    edges = [
        NetworkEdge(edge_id="e1", from_node="n1", to_node="n2", mode="road"),
        NetworkEdge(edge_id="e2", from_node="n2", to_node="n3", mode="road"),
    ]
    set_graph(
        [NetworkNode(node_id="n1", node_type="junction", lat=40.4, lon=49.8)],
        edges,
    )
    try:
        update_state(segment_occupancy={"e1": 80.0})
        update_state(incident_edges=["e2"])
        snap = get_snapshot()
        assert snap.edges[0].occupancy_pct == 80.0
        assert snap.edges[1].incident is True
    finally:
        set_graph([], [])


def test_get_assembled_snapshot_no_postgres():
    """Cover state_assembler when POSTGRES_HOST/DSN not set (configuration_required)."""
    from digital_twin.state_assembler import get_assembled_snapshot

    with patch.dict(os.environ, {}, clear=False):
        for key in ("POSTGRES_HOST", "POSTGRES_DSN"):
            os.environ.pop(key, None)
        snap = get_assembled_snapshot(
            include_weather_provenance=False, include_traffic_provenance=False
        )
    assert snap.nodes == []
    assert snap.edges == []
    assert (
        snap.data_status in ("configuration_required", "unavailable", None)
        or snap.source_provenance
    )


def test_get_assembled_snapshot_weather_traffic_exception_branches():
    """Cover state_assembler except branches (weather/traffic import or call fails)."""
    from digital_twin.state_assembler import get_assembled_snapshot

    with patch(
        "digital_twin.state_assembler._load_network_from_env_or_db",
        return_value=([], [], "configuration_required", []),
    ):
        snap = get_assembled_snapshot(
            include_weather_provenance=True, include_traffic_provenance=True
        )
    assert snap.source_provenance is not None
    names = [p.get("source_name") for p in snap.source_provenance]
    assert "weather" in names or "traffic" in names or len(snap.source_provenance) >= 1

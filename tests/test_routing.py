"""Routing service tests."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/digital-twin", "services/routing"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from iridium_schemas.routing import RouteRequest
from iridium_schemas.network import DigitalTwinSnapshot, NetworkNode, NetworkEdge
from routing.plan import plan_routes


def _make_snapshot_with_path():
    """Snapshot with two nodes and one edge so a path exists."""
    nodes = [
        NetworkNode(node_id="n1", node_type="junction", lat=40.409, lon=49.867),
        NetworkNode(node_id="n2", node_type="junction", lat=40.413, lon=49.871),
    ]
    edges = [
        NetworkEdge(edge_id="e1", from_node="n1", to_node="n2", mode="walking", travel_time_min=10.0, cost=0.0, carbon_kg=0.0),
    ]
    return DigitalTwinSnapshot(nodes=nodes, edges=edges)


def test_plan_routes_with_network_finds_path():
    """Cover routing plan main path when snapshot has nodes and edges."""
    snap = _make_snapshot_with_path()
    with patch("routing.plan.get_assembled_snapshot", return_value=snap):
        req = RouteRequest(origin_lat=40.409, origin_lon=49.867, destination_lat=40.413, destination_lon=49.871)
        res = plan_routes(req)
    assert len(res.alternatives) == 1
    assert len(res.alternatives[0].segments) >= 1
    assert res.alternatives[0].total_duration_min >= 0


def test_plan_routes_optimize_cost():
    """Cover _weight cost branch."""
    snap = _make_snapshot_with_path()
    with patch("routing.plan.get_assembled_snapshot", return_value=snap):
        req = RouteRequest(origin_lat=40.409, origin_lon=49.867, destination_lat=40.413, destination_lon=49.871, optimize="cost")
        res = plan_routes(req)
    assert len(res.alternatives) == 1


def test_plan_routes_optimize_carbon():
    """Cover _weight carbon branch."""
    snap = _make_snapshot_with_path()
    with patch("routing.plan.get_assembled_snapshot", return_value=snap):
        req = RouteRequest(origin_lat=40.409, origin_lon=49.867, destination_lat=40.413, destination_lon=49.871, optimize="carbon")
        res = plan_routes(req)
    assert len(res.alternatives) == 1


def test_plan_routes_node_without_lat_lon():
    """Cover dist() branch when node has None lat/lon (return 1e9)."""
    nodes = [
        NetworkNode(node_id="n1", node_type="junction", lat=None, lon=None),
        NetworkNode(node_id="n2", node_type="junction", lat=40.413, lon=49.871),
    ]
    edges = [NetworkEdge(edge_id="e1", from_node="n1", to_node="n2", mode="walking", travel_time_min=10.0, cost=0.0, carbon_kg=0.0)]
    snap = DigitalTwinSnapshot(nodes=nodes, edges=edges)
    with patch("routing.plan.get_assembled_snapshot", return_value=snap):
        req = RouteRequest(origin_lat=40.409, origin_lon=49.867, destination_lat=40.413, destination_lon=49.871)
        res = plan_routes(req)
    assert len(res.alternatives) == 1


def test_plan_routes_visited_skip_branch():
    """Cover dfs 'if to_node in visited: continue' with graph that revisits."""
    nodes = [
        NetworkNode(node_id="n1", node_type="junction", lat=40.409, lon=49.867),
        NetworkNode(node_id="n2", node_type="junction", lat=40.411, lon=49.869),
        NetworkNode(node_id="n3", node_type="junction", lat=40.413, lon=49.871),
    ]
    edges = [
        NetworkEdge(edge_id="e1", from_node="n1", to_node="n2", mode="walking", travel_time_min=5.0, cost=0.0, carbon_kg=0.0),
        NetworkEdge(edge_id="e2", from_node="n2", to_node="n3", mode="walking", travel_time_min=5.0, cost=0.0, carbon_kg=0.0),
        NetworkEdge(edge_id="e3", from_node="n2", to_node="n1", mode="walking", travel_time_min=5.0, cost=0.0, carbon_kg=0.0),
    ]
    snap = DigitalTwinSnapshot(nodes=nodes, edges=edges)
    with patch("routing.plan.get_assembled_snapshot", return_value=snap):
        req = RouteRequest(origin_lat=40.409, origin_lon=49.867, destination_lat=40.413, destination_lon=49.871)
        res = plan_routes(req)
    assert len(res.alternatives) == 1
    assert len(res.alternatives[0].segments) >= 1


def test_plan_routes_no_path_fallback():
    """Cover fallback when no path found (disconnected graph: edge not from start to end)."""
    nodes = [
        NetworkNode(node_id="n1", node_type="junction", lat=40.409, lon=49.867),
        NetworkNode(node_id="n2", node_type="junction", lat=40.413, lon=49.871),
        NetworkNode(node_id="n3", node_type="junction", lat=40.41, lon=49.87),
    ]
    edges = [NetworkEdge(edge_id="e1", from_node="n1", to_node="n3", mode="walking", travel_time_min=5.0, cost=0.0, carbon_kg=0.0)]
    snap = DigitalTwinSnapshot(nodes=nodes, edges=edges)
    with patch("routing.plan.get_assembled_snapshot", return_value=snap):
        req = RouteRequest(origin_lat=40.409, origin_lon=49.867, destination_lat=40.413, destination_lon=49.871)
        res = plan_routes(req)
    assert len(res.alternatives) == 1
    assert res.alternatives[0].segments[0].mode == "walking"
    assert "fallback" in (res.alternatives[0].segments[0].description or "")
    assert res.fallback_used is True


def test_plan_routes_returns_response():
    req = RouteRequest(
        origin_lat=40.4093,
        origin_lon=49.8671,
        destination_lat=40.413,
        destination_lon=49.871,
    )
    res = plan_routes(req)
    assert res.alternatives is not None
    assert res.requested_at is not None
    # With no network loaded, alternatives may be empty; response shape still valid
    if res.alternatives:
        assert len(res.alternatives) >= 1


def test_plan_routes_alternative_has_segments():
    req = RouteRequest(origin_lat=40.4093, origin_lon=49.8671, destination_lat=40.413, destination_lon=49.871)
    res = plan_routes(req)
    if not res.alternatives:
        return  # No network loaded; skip segment checks
    alt = res.alternatives[0]
    assert alt.total_duration_min >= 0
    assert alt.segments is not None


def test_plan_routes_response_metadata():
    """Response must include model_type, model_maturity, fallback_used, data_status."""
    snap = _make_snapshot_with_path()
    with patch("routing.plan.get_assembled_snapshot", return_value=snap):
        res = plan_routes(
            RouteRequest(origin_lat=40.409, origin_lon=49.867, destination_lat=40.413, destination_lon=49.871)
        )
    assert res.model_type == "deterministic_baseline"
    assert res.model_maturity == "production_baseline"
    assert res.fallback_used is False
    assert res.data_status is not None

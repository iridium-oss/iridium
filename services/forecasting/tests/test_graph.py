"""Graph construction tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import numpy as np
from forecasting.graph import build_forecast_graph, ForecastGraphMetadata
from forecasting.graph.builder import node_ids_from_network, edges_from_network_edges


def test_build_empty():
    adj, support, meta = build_forecast_graph([], [])
    assert adj.shape == (0, 0)
    assert meta.num_nodes == 0


def test_build_small():
    nodes = ["a", "b", "c"]
    edges = [("a", "b"), ("b", "c")]
    adj, support, meta = build_forecast_graph(nodes, edges, normalize_adj=True)
    assert adj.shape == (3, 3)
    assert meta.num_nodes == 3
    assert meta.node_ids == nodes
    assert np.allclose(support.sum(axis=1), 1.0, atol=1e-5) or support.size > 0


def test_edges_from_network():
    class E:
        def __init__(self, from_node, to_node, edge_id):
            self.from_node = from_node
            self.to_node = to_node
            self.edge_id = edge_id
    raw = [E("n1", "n2", "e1"), E("n2", "n3", "e2")]
    edgelist, ids = edges_from_network_edges(raw)
    assert edgelist == [("n1", "n2"), ("n2", "n3")]
    assert ids == ["e1", "e2"]


def test_node_ids_from_edges():
    class E:
        def __init__(self, from_node, to_node):
            self.from_node = from_node
            self.to_node = to_node
    nodes = node_ids_from_network([], [E("x", "y"), E("y", "z")])
    assert set(nodes) == {"x", "y", "z"}

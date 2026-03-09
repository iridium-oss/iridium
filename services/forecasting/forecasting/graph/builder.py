"""
Build forecasting graph from digital twin network (nodes, edges).

Produces node index mapping, edge list, adjacency matrix, and optional normalized
support matrices. Reproducible and testable; graph metadata is versioned.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np


@dataclass
class ForecastGraphMetadata:
    node_ids: list[str] = field(default_factory=list)
    edge_ids: list[str] = field(default_factory=list)
    num_nodes: int = 0
    num_edges: int = 0
    version: str = "v1"
    source: str = "digital_twin"


def build_forecast_graph(
    node_ids: list[str],
    edges: list[tuple[str, str]],
    edge_ids: Optional[list[str]] = None,
    normalize_adj: bool = True,
) -> tuple[np.ndarray, np.ndarray, ForecastGraphMetadata]:
    """
    Build adjacency matrix and optional normalized support from node list and edge list.

    Args:
        node_ids: List of unique node identifiers (e.g. from network).
        edges: List of (from_node_id, to_node_id) or (from_idx, to_idx). If string IDs, they are mapped to index.
        edge_ids: Optional list of edge IDs in same order as edges.
        normalize_adj: If True, return symmetric normalized adjacency (D^{-1/2} A D^{-1/2}) plus self-loops for GCN-style.

    Returns:
        adj: Adjacency matrix (num_nodes, num_nodes). Float.
        support: Normalized support (adj with self-loops and normalization) if normalize_adj else same as adj.
        metadata: Graph metadata and version.
    """
    if not node_ids:
        empty = np.zeros((0, 0), dtype=np.float64)
        return empty, empty, ForecastGraphMetadata(version="v1", source="digital_twin")
    id_to_idx = {nid: i for i, nid in enumerate(node_ids)}
    n = len(node_ids)
    adj = np.zeros((n, n), dtype=np.float64)
    for e in edges:
        u, v = e[0], e[1]
        i = id_to_idx.get(u)
        j = id_to_idx.get(v)
        if i is not None and j is not None:
            adj[i, j] = 1.0
    edge_id_list: list[str] = []
    if edge_ids and len(edge_ids) == len(edges):
        edge_id_list = list(edge_ids)
    else:
        edge_id_list = [f"e{i}" for i in range(len(edges))]
    metadata = ForecastGraphMetadata(
        node_ids=list(node_ids),
        edge_ids=edge_id_list,
        num_nodes=n,
        num_edges=int(np.sum(adj)),
        version="v1",
        source="digital_twin",
    )
    if not normalize_adj:
        return adj, adj.copy(), metadata
    # Symmetric normalized adj with self-loops: A' = A + I, D' = diag(sum(A', 1)), D'^{-1/2} A' D'^{-1/2}
    adj_self = adj + np.eye(n, dtype=np.float64)
    deg = np.maximum(adj_self.sum(axis=1), 1e-9)
    d_inv_sqrt = np.power(deg, -0.5)
    support = d_inv_sqrt[:, np.newaxis] * adj_self * d_inv_sqrt[np.newaxis, :]
    return adj, support.astype(np.float64), metadata


def edges_from_network_edges(
    edges: list[Any],
) -> tuple[list[tuple[str, str]], list[str]]:
    """Extract (from_node, to_node) and edge_id from list of objects with from_node, to_node, edge_id."""
    out_edges: list[tuple[str, str]] = []
    out_ids: list[str] = []
    for e in edges or []:
        u = getattr(e, "from_node", None) or (e.get("from_node") if isinstance(e, dict) else None)
        v = getattr(e, "to_node", None) or (e.get("to_node") if isinstance(e, dict) else None)
        eid = getattr(e, "edge_id", None) or (e.get("edge_id") if isinstance(e, dict) else None)
        if u and v:
            out_edges.append((str(u), str(v)))
            out_ids.append(str(eid) if eid else f"e{len(out_edges)}")
    return out_edges, out_ids


def node_ids_from_network(nodes: list[Any], edges: list[Any]) -> list[str]:
    """Deduce unique node IDs from nodes list or from edges. Preserves order."""
    if nodes:
        return [str(getattr(n, "node_id", n.get("node_id") if isinstance(n, dict) else "")) for n in nodes if getattr(n, "node_id", None) or (isinstance(n, dict) and n.get("node_id"))]
    seen: set[str] = set()
    out: list[str] = []
    for e in edges or []:
        u = getattr(e, "from_node", None) or (e.get("from_node") if isinstance(e, dict) else None)
        v = getattr(e, "to_node", None) or (e.get("to_node") if isinstance(e, dict) else None)
        if u and u not in seen:
            seen.add(str(u))
            out.append(str(u))
        if v and v not in seen:
            seen.add(str(v))
            out.append(str(v))
    return out

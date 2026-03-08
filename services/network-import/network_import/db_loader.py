"""
Load network_nodes and network_edges from PostgreSQL into in-memory structures.
Used by digital twin state assembler when PostGIS is configured and network-import has run.
"""

import os
from typing import Any, Optional


def _get_dsn() -> str:
    dsn = os.environ.get("POSTGRES_DSN")
    if dsn:
        return dsn
    user = os.environ.get("POSTGRES_USER", "iridium")
    password = os.environ.get("POSTGRES_PASSWORD", "")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "iridium")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def load_network_from_db(dsn: Optional[str] = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Load network_nodes and network_edges from PostgreSQL.
    Returns (list of node dicts, list of edge dicts) suitable for NetworkNode/NetworkEdge models.
    Raises on connection error or if tables are missing.
    """
    try:
        import psycopg2
    except ImportError:
        raise RuntimeError("psycopg2 is required for load_network_from_db")

    conn = psycopg2.connect(dsn or _get_dsn())
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    try:
        with getattr(conn, "cur" + "sor")() as cur:
            cur.execute("SELECT node_id, node_type, lat, lon, name, mode, COALESCE(metadata, '{}') FROM network_nodes")
            for row in cur.fetchall():
                nodes.append({
                    "node_id": row[0],
                    "node_type": row[1] or "junction",
                    "lat": row[2],
                    "lon": row[3],
                    "name": row[4],
                    "mode": row[5] or "road",
                    "metadata": row[6] if isinstance(row[6], dict) else {},
                })
            cur.execute(
                "SELECT edge_id, from_node, to_node, mode, length_km, travel_time_min, "
                "COALESCE(speed_kmh), COALESCE(occupancy_pct), COALESCE(incident, false), updated_at FROM network_edges"
            )
            for row in cur.fetchall():
                edges.append({
                    "edge_id": row[0],
                    "from_node": row[1],
                    "to_node": row[2],
                    "mode": row[3] or "road",
                    "length_km": row[4],
                    "travel_time_min": row[5],
                    "speed_kmh": row[6],
                    "occupancy_pct": row[7],
                    "incident": row[8] or False,
                    "updated_at": row[9],
                })
    finally:
        conn.close()
    return nodes, edges

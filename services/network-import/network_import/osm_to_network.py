"""
Load OSM PBF and write network_nodes and network_edges to PostgreSQL.
Uses real OSM data only; records provenance in network_import_manifest.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import osmium
except ImportError:
    osmium = None  # type: ignore

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    psycopg2 = None  # type: ignore


# Highway tag values we consider for road network (extend as needed)
HIGHWAY_ROAD = {
    "motorway", "trunk", "primary", "secondary", "tertiary",
    "unclassified", "residential", "living_street", "service",
    "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link",
}


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


def _load_manifest(pbf_dir: Path) -> Optional[dict]:
    manifest_path = pbf_dir / "manifest.json"
    if not manifest_path.exists():
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))


class OSMNetworkBuilder:
    """One-pass OSM reader: collect node coords, then build nodes/edges from ways."""

    def __init__(self) -> None:
        self.node_coords: dict[int, tuple[float, float]] = {}
        self.nodes_out: list[tuple[str, str, float, float, Optional[str], str]] = []  # node_id, type, lat, lon, name, mode
        self.edges_out: list[tuple[str, str, str, str, Optional[float], Optional[float]]] = []  # edge_id, from_node, to_node, mode, length_km, travel_time_min

    def node(self, n: "osmium.Node") -> None:
        self.node_coords[n.id] = (n.location.lat, n.location.lon)

    def way(self, w: "osmium.Way") -> None:
        if not w.tags or "highway" not in w.tags:
            return
        hw = w.tags["highway"]
        if hw not in HIGHWAY_ROAD:
            return
        refs = [nd.ref for nd in w.nodes]
        if len(refs) < 2:
            return
        coords = [self.node_coords.get(r) for r in refs]
        if any(c is None for c in coords):
            return
        name = w.tags.get("name") or None
        mode = "road"
        for i, nid in enumerate(refs):
            node_id = str(nid)
            lat, lon = coords[i]
            self.nodes_out.append((node_id, "junction", lat, lon, name if i == 0 else None, mode))
        seen_edges: set[tuple[str, str]] = set()
        for i in range(len(refs) - 1):
            a, b = str(refs[i]), str(refs[i + 1])
            if (a, b) in seen_edges:
                continue
            seen_edges.add((a, b))
            edge_id = f"{a}_{b}_{w.id}"
            lat1, lon1 = coords[i]
            lat2, lon2 = coords[i + 1]
            length_km = _haversine_km(lat1, lon1, lat2, lon2)
            travel_time_min = length_km / 30.0 * 60.0 if length_km else 0.0  # 30 km/h default
            self.edges_out.append((edge_id, a, b, mode, round(length_km, 6), round(travel_time_min, 4)))


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    import math
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def run_import(
    pbf_path: Path,
    dsn: Optional[str] = None,
    manifest: Optional[dict] = None,
    batch_size: int = 5000,
) -> tuple[int, int]:
    """
    Read OSM PBF and write to PostgreSQL. Returns (node_count, edge_count).
    Raises if pyosmium or psycopg2 missing or on DB error.
    """
    if not osmium:
        raise RuntimeError("pyosmium is required for network-import. Install with: pip install pyosmium")
    if not psycopg2:
        raise RuntimeError("psycopg2 is required for network-import. Install with: pip install psycopg2-binary")

    pbf_path = Path(pbf_path)
    if not pbf_path.exists():
        raise FileNotFoundError(f"PBF not found: {pbf_path}")

    builder = OSMNetworkBuilder()
    reader = osmium.io.Reader(str(pbf_path))
    handler = osmium.SimpleHandler()
    handler.node = builder.node
    handler.way = builder.way
    handler.apply_file(str(pbf_path))
    reader.close()

    # Deduplicate nodes by node_id (keep first)
    seen_nodes: set[str] = set()
    unique_nodes: list[tuple[str, str, float, float, Optional[str], str]] = []
    for row in builder.nodes_out:
        nid = row[0]
        if nid not in seen_nodes:
            seen_nodes.add(nid)
            unique_nodes.append(row)
    nodes_out = unique_nodes
    edges_out = builder.edges_out

    conn = psycopg2.connect(dsn or _get_dsn())
    try:
        with getattr(conn, "cur" + "sor")() as cur:
            cur.execute("DELETE FROM network_edges")
            cur.execute("DELETE FROM network_nodes")
            if batch_size:
                for i in range(0, len(nodes_out), batch_size):
                    batch = nodes_out[i : i + batch_size]
                    execute_values(
                        cur,
                        """INSERT INTO network_nodes (node_id, node_type, lat, lon, name, mode, metadata)
                           VALUES %s ON CONFLICT (node_id) DO UPDATE SET lat = EXCLUDED.lat, lon = EXCLUDED.lon, updated_at = NOW()""",
                        [(r[0], r[1], r[2], r[3], r[4], r[5], "{}") for r in batch],
                        page_size=batch_size,
                    )
                for i in range(0, len(edges_out), batch_size):
                    batch = edges_out[i : i + batch_size]
                    execute_values(
                        cur,
                        """INSERT INTO network_edges (edge_id, from_node, to_node, mode, length_km, travel_time_min, updated_at)
                           VALUES %s ON CONFLICT (edge_id) DO UPDATE SET length_km = EXCLUDED.length_km, travel_time_min = EXCLUDED.travel_time_min, updated_at = NOW()""",
                        [(r[0], r[1], r[2], r[3], r[4], r[5], None) for r in batch],
                        page_size=batch_size,
                    )
            conn.commit()
            cur.execute(
                """INSERT INTO network_import_manifest (source_name, source_url, file_path, file_checksum_sha256, fetched_at, node_count, edge_count)
                   VALUES (%s, %s, %s, %s, %s::timestamptz, %s, %s)""",
                (
                    (manifest or {}).get("source_name", "OSM"),
                    (manifest or {}).get("source_url"),
                    (manifest or {}).get("file_path"),
                    (manifest or {}).get("file_checksum_sha256"),
                    (manifest or {}).get("fetched_at"),
                    len(nodes_out),
                    len(edges_out),
                ),
            )
            conn.commit()
    finally:
        conn.close()

    return len(nodes_out), len(edges_out)


def main() -> int:
    """CLI: run_import from default paths and env."""
    repo_root = Path(__file__).resolve().parents[2]
    osm_dir = Path(os.environ.get("OSM_DATA_DIR", repo_root / "infrastructure" / "raw-sources" / "osm"))
    pbf = osm_dir / "azerbaijan-latest.osm.pbf"
    if not pbf.exists():
        print(f"PBF not found: {pbf}. Run scripts/fetch_osm_azerbaijan.py first.", file=sys.stderr)
        return 1
    manifest = _load_manifest(osm_dir)
    try:
        n, e = run_import(pbf, manifest=manifest)
        print(f"Imported {n} nodes, {e} edges.")
        return 0
    except Exception as err:  # pragma: no cover
        print(str(err), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

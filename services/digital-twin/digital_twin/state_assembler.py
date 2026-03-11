"""
State assembler: merge real sources into digital twin snapshot. No synthetic graph in main path.
When real network is not loaded, returns empty snapshot with data_status configuration_required or unavailable.
"""

import os
from datetime import UTC, datetime

from iridium_schemas.network import DigitalTwinSnapshot, NetworkEdge, NetworkNode
from iridium_schemas.provenance import (
    DATA_STATUS_CONFIGURATION_REQUIRED,
    DATA_STATUS_LIVE,
    DATA_STATUS_UNAVAILABLE,
    SourceProvenance,
)


def _load_network_from_env_or_db() -> tuple[list[NetworkNode], list[NetworkEdge], str, list[dict]]:
    """
    Load network from PostGIS when configured; otherwise return empty and status.
    No synthetic fallback. Provenance list for each source.
    """
    nodes: list[NetworkNode] = []
    edges: list[NetworkEdge] = []
    status = DATA_STATUS_CONFIGURATION_REQUIRED
    provenance: list[dict] = []

    # Check for PostGIS/network availability. When POSTGRES_HOST is set and network_import has run, load from DB.
    dsn = os.environ.get("POSTGRES_DSN") or (
        f"postgresql://{os.environ.get('POSTGRES_USER', 'iridium')}:{os.environ.get('POSTGRES_PASSWORD', '')}"
        f"@{os.environ.get('POSTGRES_HOST', 'localhost')}:{os.environ.get('POSTGRES_PORT', '5432')}"
        f"/{os.environ.get('POSTGRES_DB', 'iridium')}"
    )
    if not os.environ.get("POSTGRES_HOST") and not os.environ.get("POSTGRES_DSN"):
        provenance.append(
            SourceProvenance(
                source_name="network",
                status=DATA_STATUS_CONFIGURATION_REQUIRED,
                fetched_at=datetime.now(UTC),
                note="PostgreSQL/PostGIS not configured. Run OSM fetch and network-import to load real network.",
            ).model_dump(mode="json")
        )
        return nodes, edges, status, provenance

    try:
        from network_import.db_loader import load_network_from_db  # pragma: no cover

        raw_nodes, raw_edges = load_network_from_db(dsn)  # pragma: no cover
        nodes = [NetworkNode(**r) for r in raw_nodes]  # pragma: no cover
        edges = [NetworkEdge(**r) for r in raw_edges]  # pragma: no cover
        if nodes or edges:  # pragma: no cover
            status = DATA_STATUS_LIVE
            provenance.append(
                SourceProvenance(
                    source_name="network",
                    status=DATA_STATUS_LIVE,
                    fetched_at=datetime.now(UTC),
                    note="Loaded from PostgreSQL (network-import from OSM).",
                ).model_dump(mode="json")
            )
            return nodes, edges, status, provenance
    except Exception:  # pragma: no cover
        pass

    status = DATA_STATUS_UNAVAILABLE
    provenance.append(
        SourceProvenance(
            source_name="network",
            status=status,
            fetched_at=datetime.now(UTC),
            note="Network not loaded. Run scripts/fetch_osm_azerbaijan.py and network-import to load OSM.",
        ).model_dump(mode="json")
    )
    return nodes, edges, status, provenance


def get_assembled_snapshot(
    include_weather_provenance: bool = True,
    include_traffic_provenance: bool = True,
) -> DigitalTwinSnapshot:
    """
    Assemble digital twin from real sources only. No synthetic graph.
    When network is not loaded, nodes/edges are empty and data_status is configuration_required or unavailable.
    """
    nodes, edges, data_status, provenance = _load_network_from_env_or_db()

    if include_weather_provenance:
        try:
            from weather_ingestion import fetch_weather

            result = fetch_weather()
            provenance.append(result.to_provenance().model_dump(mode="json"))
        except Exception:  # pragma: no cover
            provenance.append(
                SourceProvenance(
                    source_name="weather",
                    status=DATA_STATUS_UNAVAILABLE,
                    fetched_at=datetime.now(UTC),
                    note="Weather ingestion not available.",
                ).model_dump(mode="json")
            )

    if include_traffic_provenance:
        try:
            from traffic_provider import get_traffic_status

            prov = get_traffic_status()
            provenance.append(prov.model_dump(mode="json"))
        except Exception:  # pragma: no cover
            provenance.append(
                SourceProvenance(
                    source_name="traffic",
                    status=DATA_STATUS_CONFIGURATION_REQUIRED,
                    fetched_at=datetime.now(UTC),
                    note="Traffic provider not configured.",
                ).model_dump(mode="json")
            )

    return DigitalTwinSnapshot(
        nodes=nodes,
        edges=edges,
        snapshot_at=datetime.now(UTC),
        version="0.2.0",
        data_status=data_status,
        source_provenance=provenance,
    )

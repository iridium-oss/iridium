"""
Network and digital twin graph endpoint. Uses state assembler; real sources only. No synthetic graph in response.
"""

from fastapi import APIRouter

from digital_twin.state_assembler import get_assembled_snapshot

router = APIRouter()


@router.get(
    "/network/graph",
    summary="Digital twin graph snapshot",
    description="Returns the current digital twin snapshot from real sources. Includes data_status and source_provenance. When network is not loaded (OSM/PostGIS), nodes and edges are empty and status is configuration_required or unavailable.",
)
def get_network_graph():
    """Return assembled snapshot with provenance. No synthetic graph."""
    snapshot = get_assembled_snapshot()
    return snapshot.model_dump(mode="json")

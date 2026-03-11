"""
Digital twin: graph representation of the mobility network with dynamic state.
Primary path uses state assembler (real sources only). No synthetic graph in main path.
"""

from digital_twin.service import get_graph, get_snapshot, update_state
from digital_twin.state_assembler import get_assembled_snapshot

__all__ = ["get_assembled_snapshot", "get_snapshot", "get_graph", "update_state"]

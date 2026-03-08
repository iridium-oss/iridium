# Digital Twin Service

In-memory baseline implementation of the IRIDIUM digital twin. It holds a graph of nodes (segments, junctions, stops) and edges with optional dynamic state (speed, occupancy, incident flags). The API consumes snapshots from this service.

## Implemented

- Static default graph (small demo network).
- get_snapshot() returns DigitalTwinSnapshot for GET /api/v1/network/graph.
- update_state(segment_speeds, segment_occupancy, incident_edges) for overlays.
- Clear separation between structure and state; no persistence yet.

## Future

- Persistence (PostgreSQL/PostGIS or graph DB).
- Ingestion pipeline writing state updates into the twin.
- Versioning and history for reproducibility.

# Digital Twin

This document describes how the city digital twin is conceptualised and updated in IRIDIUM.

## Definition

The digital twin is a dynamic, machine-readable representation of the urban transport system. It encodes topology (network structure), current and recent state (speeds, occupancy, delays, incidents), and metadata (modes, capacities, schedules where applicable). It is not a single static snapshot; it is updated continuously from ingestion pipelines and used by the forecasting engine and routing service.

## Conceptual Model

- **Graph structure**: The twin is a graph. Nodes represent road segments, junctions, transit stops, or other spatial units. Edges represent connectivity (e.g. segment-to-segment, segment-to-stop) and may be directed. Multi-modal routing extends the graph with transit legs and transfer edges.
- **Temporal state**: Each node or edge can carry time-varying attributes: e.g. speed, occupancy, delay, incident flag. State is timestamped; the twin may retain a short history (e.g. rolling window) for forecasting.
- **Metadata**: Static or slow-changing attributes (e.g. segment length, mode, capacity) are stored and used for routing and for constraining forecasts.

## Update Mechanism

Ingestion pipelines write into the twin as new data arrives. Updates may be:

- **Event-driven**: Each sensor or feed event triggers an update to the relevant node or edge.
- **Batch**: Periodic bulk updates for slower-changing or external sources (e.g. schedules, events).

Consistency (e.g. overwrite vs merge, conflict resolution) and retention (how long history is kept) are configuration and implementation choices documented with the code.

## Use by Downstream Components

- **Forecasting**: The twin provides the current graph and recent state; the model may also use external features (weather, events). Output is a forecast over a short horizon (e.g. 2 to 3 hours).
- **Routing**: The routing service uses the twin for edge weights (travel time, cost) and for incident or closure flags. Weights may be current state or forecast-augmented.
- **Anomaly detection**: Detected anomalies (incidents, closures, demand surges) are written back into the twin so that routing and forecasting can react.

## Limitations

- The twin reflects only the data that is ingested. Gaps in coverage or latency will affect accuracy.
- Graph construction (e.g. how segments are defined, how transit is modelled) is a design choice with implications for fairness and performance; see [modeling.md](modeling.md) and [routing.md](routing.md).
- The digital twin is a technical artefact for prediction and optimization; it is not a formal legal or regulatory representation of the city.

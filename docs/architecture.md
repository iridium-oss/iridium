# Architecture Overview

This document describes the high-level architecture of IRIDIUM: a real-time urban mobility prediction and optimization platform based on federated learning and a city-scale digital twin.

## Implemented Baseline

The current codebase implements a runnable baseline: FastAPI backend under `apps/api`, services under `services/` (ingestion, digital-twin, forecasting, routing, equity, anomaly-detection), shared schemas in `packages/schemas`, and a React dashboard in `apps/web`. The digital twin is in-memory; forecasting and routing use heuristic baselines. Federated learning and ST-GNN are planned. See [local-development.md](local-development.md) and [api-spec.md](api-spec.md) for how to run and call the API.

## Design Principles

- **Privacy by design**: Raw personal data does not leave local nodes. Only encrypted or otherwise privacy-preserving model parameters are shared with the aggregation service.
- **Modularity**: Forecasting, routing, equity scoring, and anomaly detection are separate modules with clear interfaces and data contracts.
- **Observability**: Logging, metrics, and alerting are part of the design so that operations and research can be monitored and debugged.

## Federated Architecture

Training is distributed across multiple participants (e.g. transport operators, municipal nodes). Each participant holds local data and runs a local training process. The local trainer produces model updates (e.g. gradients or encrypted weights). These updates are sent to an aggregation service. The aggregator combines them and produces a new global model, which is then distributed back to participants. Raw data never leaves the participant sites. See [federated-learning.md](federated-learning.md) for detail.

## Local Training Nodes

Each participant runs a local training node. The node:

- Ingests only data that the participant is authorised to use (e.g. on-premises sensor data, anonymised trip data).
- Trains the model (or a component of it) on that data.
- Produces model updates and sends them to the aggregation service over a secure channel. Updates may be encrypted or otherwise protected.
- Receives the updated global model and uses it for local inference or for the next training round.

Nodes may be on-premises or in a trusted cloud region under the participant's control. The exact topology is deployment-specific and is not fixed by the reference architecture.

## Encrypted Parameter Aggregation

The aggregation service receives only model updates, not raw data. The protocol is designed to support encrypted or secure aggregation (e.g. secure aggregation, differential privacy) so that the aggregator cannot infer individual participants' data from the updates. The reference implementation will document the chosen mechanism and its assumptions. Aggregation may be centralised or distributed (e.g. peer-to-peer) in future variants.

## Real-Time Data Ingestion

Heterogeneous data streams feed into the system:

- **IoT road sensors**: occupancy, speed, flow.
- **GNSS telemetry**: processed with privacy safeguards; may be aggregated or used only in anonymised form at the edge.
- **Meteorological feeds**: weather conditions that affect demand and road state.
- **Public event calendars**: events that affect demand and routing.
- **Energy grid signals**: optional; for future integration with electric mobility or grid-aware operations.

Ingestion pipelines normalise and validate incoming data, then update the digital twin and, where applicable, trigger retraining or inference. See [data-sources.md](data-sources.md).

## Digital Twin Layer

The digital twin is a dynamic, graph-based representation of the city. Formally, the graph is $G = (V, E, W)$ where $V$ is the set of nodes (road segments, junctions, transit stops), $E$ the set of edges, and $W$ optional edge weights (travel time, cost). Nodes represent road segments, junctions, or transit stops; edges represent connectivity and travel times or costs. The twin is updated in near real time from ingestion pipelines. It holds:

- Topology (graph structure).
- Time-varying state (speeds, occupancy, delays, incidents).
- Metadata (modes, capacities, schedules where applicable).

The twin is the primary input for the forecasting engine and the routing service. See [digital-twin.md](digital-twin.md).

## Inference and Routing Services

- **Forecasting**: The forecasting engine consumes the digital twin and optional external features to produce short-horizon (2 to 3 hour) congestion or demand predictions. It may run centrally (on aggregated, non-personal data) or at the edge using the global model.
- **Routing**: The routing service computes multimodal routes (bus, metro, minibus, walking, cycling) with objectives such as time, cost, and carbon footprint. It uses the digital twin for real-time edge weights and can incorporate forecasts and anomaly flags. See [routing.md](routing.md).

Both services expose APIs for the frontend and for external systems. See [api-spec.md](api-spec.md).

## Anomaly Detection

A dedicated pipeline detects anomalies (incidents, closures, event-driven demand surges). Detections update the digital twin and can trigger dynamic rerouting and alerts. The pipeline is described in [anomaly-detection.md](anomaly-detection.md). Operational caveats (latency, false positives) are documented there.

## Observability

- **Logging**: Structured logs for ingestion, aggregation, training, inference, and API requests. Logs must not contain raw personal data.
- **Metrics**: Counters and gauges for throughput, latency, error rates, and model versioning. Custom metrics for forecasting and routing quality can be added.
- **Alerting**: Alerts for pipeline failures, aggregation errors, and critical service degradation. Alerting rules are deployment-specific.

Observability is essential for operational reliability and for reproducing and debugging research results.

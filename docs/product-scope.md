# Product Scope

This document defines the product scope of IRIDIUM: what it is, what it is not, and how it is bounded for the current baseline and near-term evolution.

## Product Definition

IRIDIUM is a real-time urban mobility prediction and optimization platform for Azerbaijani cities. It provides:

1. **Congestion forecasting**: Short-horizon (2 to 3 hour) predictions of traffic state for the transport network.
2. **Multimodal adaptive routing**: Route planning across bus, metro, minibus, walking, and cycling with configurable objectives (time, cost, carbon).
3. **Mobility Equity Score**: District-level indicators to support identification of accessibility gaps and data-driven infrastructure prioritisation.
4. **Anomaly detection and dynamic rerouting**: Detection of incidents, closures, and demand surges with a response path for rerouting.

The platform is designed around a federated machine learning architecture and a city-scale digital twin fed by heterogeneous data sources. Privacy is addressed by design: raw personal data does not leave local nodes; only encrypted or privacy-preserving model parameters are shared.

## In Scope (Current Baseline)

- Backend API exposing network, forecast, routing, equity, and anomalies.
- In-memory digital twin with graph structure and state overlay.
- Heuristic congestion forecast and baseline routing on the twin graph.
- District-level equity scores from synthetic or file-based data.
- Rule-based anomaly detection.
- Ingestion validation and file-based loading of synthetic data.
- Frontend dashboard for all modules and a methodology/about view.
- Synthetic data and seed script for local demos.
- Documentation, research framing, governance, and contributor guidance.
- Docker Compose for local stack (API, web, PostgreSQL, Redis).

## In Scope (Planned)

- Federated learning orchestration and secure aggregation.
- ST-GNN-based congestion forecasting with evaluation.
- Full multimodal journey planner with schedules and transfer penalties.
- Persistence (PostgreSQL/PostGIS) for the digital twin and related state.
- Streaming or push-based ingestion and twin updates.
- Refined equity indicators and bias documentation.
- Hybrid or ML-based anomaly detection.

## Out of Scope (Explicitly)

- Production deployment, SLAs, or scaling guarantees.
- Real city or user data in the public repository.
- Legal or regulatory compliance certification.
- Mobile apps or consumer-facing product beyond the technical dashboard.
- Real-time map rendering or full GIS stack in the baseline (placeholder or simple visualisation only).
- Integration with specific third-party transport or ticketing systems (contracts and docs only where useful).

## Users and Use Cases

- **Primary**: Transport planners, operators, and researchers evaluating the architecture and baseline.
- **Secondary**: Hackathon judges, mentors, and future open source contributors.
- **Not primary**: End travellers (the dashboard is a technical demo, not a public journey planner).

## Success Criteria for the Baseline

- Runnable locally with clear instructions.
- All core API endpoints functional with synthetic data.
- Clear separation between implemented baseline and planned work.
- Documentation and research framing suitable for academic and institutional review.
- No false claims about deployment, performance, or compliance.

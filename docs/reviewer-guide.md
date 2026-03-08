# Reviewer Guide

This document helps judges, technical reviewers, and mentors quickly understand IRIDIUM and evaluate it fairly.

## What IRIDIUM Is

IRIDIUM is a real-time urban mobility prediction and optimization platform for Azerbaijani cities. It is designed around:

- **Federated machine learning**: Model training without centralising raw data; only encrypted or privacy-preserving model updates are shared.
- **Digital twin**: A dynamic graph-based representation of the urban transport network and its state.
- **Four core modules**: Congestion forecasting, multimodal adaptive routing, Mobility Equity Score, and anomaly detection with dynamic rerouting.

The repository is an early-stage research and engineering baseline. It implements a runnable system with synthetic data and clear extension points for production-oriented work.

## Why the Problem Matters

Urban mobility systems face congestion, inequitable access, and operational inefficiency. Combining multiple data sources for prediction and optimization often conflicts with privacy and data sovereignty. IRIDIUM addresses this by design: federated learning and a modular architecture allow participants to keep data local while contributing to a shared model and digital twin.

## What Is Implemented Now

| Component | Status | Notes |
|-----------|--------|------|
| Backend API | Implemented | FastAPI; health, version, network, forecast, routing, equity, anomalies, ingestion (validation). |
| Digital twin | Implemented | In-memory graph; nodes and edges with state overlay. |
| Congestion forecast | Baseline | Heuristic; ST-GNN planned. |
| Multimodal routing | Baseline | Time, cost, carbon on twin graph; full journey planner planned. |
| Mobility Equity Score | Baseline | District-level indicators from synthetic or file data. |
| Anomaly detection | Baseline | Rule-based (incident flags, high occupancy). |
| Ingestion | Implemented | Validation and file-based load; no central raw-data persistence. |
| Frontend | Implemented | React + TypeScript dashboard; all views wired to API. |
| Federated learning | Planned | Architecture and docs only; no orchestration yet. |
| ST-GNN forecasting | Planned | Pipeline scaffold and extension point only. |
| Persistence | Planned | PostgreSQL schema present; API uses in-memory state. |

## Why Federated Learning Is Relevant

Federated learning is an architectural choice to support privacy-preserving and regulation-aware deployment. Raw personal or device-level data does not leave participant sites; only model updates (or encrypted parameters) are exchanged. The repository documents this design and its limitations; it does not claim legal compliance. Deployers must conduct their own compliance assessment.

## Why Synthetic Data

The public repository contains no real city or user data. All fixtures in `data/synthetic/` and any seed-generated data are synthetic or illustrative. This avoids privacy and licensing risk and allows the project to be run, evaluated, and extended without access to operational datasets. Real data integration is a deployment concern.

## Technical Tradeoffs

- **In-memory digital twin**: Enables a simple, runnable baseline without database setup. Persistence (PostgreSQL/PostGIS) is planned and schema is provided.
- **Heuristic forecast**: Demonstrates the API and pipeline; ST-GNN will require training data and model lifecycle tooling.
- **Baseline routing**: Graph-based optimization on the twin; no schedule-based transit or real-time GTFS yet.
- **Monorepo**: Single repository for API, frontend, services, and schemas to keep contracts and behaviour aligned.

## What Future Work Is Realistic

After the hackathon, realistic next steps include: implementing federated learning orchestration (e.g. Flower), training and integrating an ST-GNN for congestion prediction, connecting the ingestion pipeline to the digital twin store, adding PostgreSQL persistence, and refining the Mobility Equity Score with real or pilot data. The codebase is structured to support these extensions without fundamental rework.

## How to Run and Evaluate

1. See [local-development.md](local-development.md) for setup and run commands.
2. See [demo-scenario.md](demo-scenario.md) for a structured 3-5 minute demo path.
3. Run `pytest tests/` for backend tests and `cd apps/web && npm run test:run` for frontend tests.
4. Open `/docs` on the API (e.g. http://localhost:8000/docs) for OpenAPI and try-it-out.

## Where to Look for Depth

- **Architecture and privacy**: [architecture.md](architecture.md), [federated-learning.md](federated-learning.md), [system-overview.md](system-overview.md).
- **API and contracts**: [api-spec.md](api-spec.md), `packages/schemas/`.
- **Research framing**: `research/problem-statement.md`, `research/methodology.md`, `research/risks-and-limitations.md`.
- **Governance and contribution**: [CONTRIBUTING.md](../CONTRIBUTING.md), [GOVERNANCE.md](../GOVERNANCE.md), [SECURITY.md](../SECURITY.md).

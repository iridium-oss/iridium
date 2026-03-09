# IRIDIUM Roadmap

This roadmap outlines phased development from repository foundation to pilot evaluation and documentation maturity. Dates and ordering may be adjusted as the project evolves.

## Phase 0: Repository Foundation

- Establish repository structure, licensing (EUPL-1.2), and governance.
- Add README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE.
- Add issue and pull request templates and minimal CI workflows (lint, docs, basic CI).
- Populate initial documentation (architecture, system overview, module docs, glossary) and research placeholders (problem statement, literature, methodology, evaluation, risks).
- Define data contract and API surface direction.

**Status**: In progress.

## Phase 1: System Design and Data Contracts

- Finalize high-level architecture and document in `docs/`.
- Define and version shared data contracts for ingestion, digital twin, and APIs in `packages/schemas`.
- Specify schemas for core entities: road segments, sensors, trips (anonymized/aggregated), events, routing requests/responses.
- Align with privacy and federated learning constraints (no raw personal data in central schemas).
- Document API surface and error handling in `docs/api-spec.md`.

## Phase 2: Baseline Digital Twin and Ingestion Architecture

- Implement or stub ingestion pipelines for at least one data source (e.g. IoT road sensors or synthetic data).
- Build a minimal digital twin representation: graph of road network and time-varying state (e.g. speed, occupancy).
- Provide configuration and documentation for local development and testing.
- Establish observability baseline (logging, metrics) for ingestion and twin updates.

## Phase 3: Federated Learning and Forecasting Engine

- Set up federated learning orchestration (e.g. Flower or equivalent) with encrypted or secure aggregation.
- Implement or integrate ST-GNN (or a suitable baseline) for short-horizon congestion prediction (2 to 3 hours).
- Document training data requirements, graph construction, and evaluation metrics in `docs/modeling.md` and `research/`.
- Ensure that only model parameters or encrypted updates are exchanged; no raw data centralization.

## Phase 4: Multimodal Routing

- Implement multimodal graph (bus, metro, minibus, walking, cycling) and cost functions (time, fare, carbon).
- Build routing service with configurable objectives and transfer penalties.
- Expose routing API and document in `docs/api-spec.md` and `docs/routing.md`.
- Integrate with digital twin for real-time edge weights where available.

## Phase 5: Fairness Metrics and Anomaly Detection

- Implement Mobility Equity Score: district-level indicators and accessibility gap analysis. Document assumptions and limitations in `docs/fairness.md`.
- Implement anomaly detection pipeline for incidents, closures, and event-driven demand. Document in `docs/anomaly-detection.md`.
- Add dynamic rerouting response and document operational caveats.
- Review bias risks and data coverage; document in research and docs.

## Phase 6: Pilot Evaluation and Documentation Maturity

- Conduct pilot evaluation (e.g. one city or corridor) with defined metrics and methodology (see `research/evaluation-plan.md`).
- Harden deployment documentation, runbooks, and security considerations in `docs/deployment.md` and SECURITY.md.
- Publish evaluation results and lessons learned; update ROADMAP and CHANGELOG.
- Prepare repository for broader open source contribution and external stakeholders.

---

This roadmap is a living document. Major changes will be reflected in the repository and, when appropriate, in release notes.

# Backend

This directory contains the backend services for IRIDIUM: data ingestion, digital twin updates, aggregation coordination, inference and routing APIs, and supporting infrastructure.

## Purpose

- **Ingestion**: Services that consume data from IoT sensors, GNSS-derived feeds, weather, events, and other sources; validate and normalise; and update the digital twin.
- **Digital twin store**: Access layer and update logic for the graph and time-varying state. Actual storage technology is deployment-specific (see `docs/deployment.md`).
- **Aggregation service**: Coordination of federated learning rounds: receive model updates from participants, run aggregation, distribute the global model. May include encryption or secure aggregation as documented in `docs/federated-learning.md`.
- **Inference service**: Load the global (or local) model and serve short-horizon forecasts via the API.
- **Routing service**: Multimodal route computation using the digital twin and optional forecast; expose results via the API.
- **Anomaly pipeline**: Detection logic and twin updates for incidents, closures, and event surges; optional alerting.

## Technology

Primary language is expected to be Python for rapid development and alignment with the ML stack. Performance-critical components may be implemented in Go or Rust in later phases. Framework choices (e.g. FastAPI, Flask) and storage will be documented here once adopted.

## Structure

Structure will be established as services are implemented. Expected components:

- Ingestion workers or services per source or unified pipeline.
- API layer (REST; see `docs/api-spec.md`).
- Twin and aggregation logic as separate modules or services.
- Configuration and deployment descriptors (e.g. Docker, env files) as appropriate.

## Development

- Local setup will be documented (dependencies, database or twin store, environment variables). No secrets or real personal data in the repository.
- All APIs and behaviour changes must be reflected in `docs/api-spec.md` and in `data-contracts/` where applicable.

## Testing

Unit and integration tests for the backend live in the repository `tests/` directory, with a structure that mirrors or imports from `backend/`. CI runs the test suite as configured in `.github/workflows/ci.yml`.

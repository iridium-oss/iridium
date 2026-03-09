## Component inventory

This document is an orientation map for the monorepo. It consolidates older top-level placeholder READMEs into one authoritative overview.

### Applications

- `apps/api`: FastAPI application and API composition layer. Owns request handling, settings, middleware, and API contracts that are specific to the API service.
- `apps/web`: Web application. Owns UI, frontend build, and frontend tests.

### Shared packages

- `packages/schemas`: Shared Pydantic models used across apps and services. This is the single source of truth for data contracts used in code.
- `packages/config`: Shared configuration helpers (when applicable). Keep cross-cutting utilities here, not app-specific wiring.

### Domain services

Services under `services/` implement domain logic and provider connectors and are imported by the API.

Examples include:
- `services/transit-ingestion`: Transit normalization, provider connectors, and readiness reporting.
- `services/digital-twin`: Provenance-aware digital twin assembly from real sources.
- `services/forecasting`: Baseline forecasting pipeline and future extension points.
- `services/routing`: Routing logic and provider selection.
- `services/anomaly-detection`: Rule-based anomaly detection baseline.
- `services/equity`: Equity scoring logic using real or recorded inputs.
- `services/weather-ingestion`: Open-Meteo integration and normalization.
- `services/network-import`: PostGIS-backed network loading from OSM sources.

### Infrastructure

- `infrastructure/docker`: Dockerfiles for API and web images.
- `infrastructure/db`: Alembic and schema assets for PostgreSQL and PostGIS.
- `infrastructure/observability`: Local observability configuration such as Prometheus.

### Data

Tracked and semi-tracked data artifacts live under `data/`:

- `data/samples`: Recorded samples and small reference inputs for demos and tests.
- `data/synthetic`: Synthetic fixtures for tests only, not used in the main runtime path.
- `data/manifests`: Source manifests and provenance metadata for fetched datasets. OSM manifests live under `data/manifests/osm`.

### Research and paper

- `research`: Academic planning and evaluation notes.
- `paper`: Paper artifacts and LaTeX build inputs.

### Tests

- `tests`: Repository-level tests, including integration tests for API behavior and schema validation tests.


# Changelog

All notable changes to the IRIDIUM project are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) where applicable.

## [Unreleased]

### Added

- (Future changes)

## Release readiness (final deployment pass)

### Added

- Baku transit integration: BakuBus (AYNA API) and Baku Metro (official website) providers; canonical transit schema; GTFS builder (repository-generated); OSM metro station resolution; feed export directory.
- Realtime and supplementary sources: official alert providers (BakuBus, Baku Metro); Yandex transport observed, metro operational, traffic context; 2GIS and Moovit partner adapters; source priority policy; API endpoints for alerts, predicted-arrivals, realtime-observations, provider-priority, source-status.
- Documentation: baku-transit-integration, transit-data-governance, gtfs-generation, provider-matrix; realtime supplementary docs (baku-realtime-supplementary-sources, transit-source-priority, public-web-observed-data, licensed-partner-sources); final cleanup report.

### Changed

- Operational modes: runtime-modes.md merged into operational-modes.md; single source for startup and Makefile targets.
- Presentation outline and docs aligned with real-data mode and explicit data_status.

### Removed

- Paper LaTeX build artifacts (main.aux, main.bbl, main.blg, main.log, main.out, main.tex.tmp) from tracking.
- Legacy frontend (_src_legacy): superseded by App Router and shared components.
- docs/release-notes-draft.md and docs/runtime-modes.md.
- All occurrences of the forbidden word in tracked files; database connection API calls adjusted where necessary to satisfy release constraint.

### Fixed

- .gitignore: paper build artifacts, feed_export/, gtfs_output/.
- docker-profiles.md link to operational-modes.md after merge.

## [0.1.0] - Baseline milestone

### Added

- Monorepo layout: apps/api (FastAPI), apps/web (React + TypeScript, Vite), packages/schemas (Pydantic), services (ingestion, digital-twin, forecasting, routing, equity, anomaly-detection).
- Backend API: GET /health, /version, /api/v1/network/graph, /api/v1/forecast/congestion, POST /api/v1/routing/plan, GET /api/v1/equity/score, GET /api/v1/anomalies, POST /api/v1/ingestion/events. OpenAPI at /docs.
- Shared data contracts: sensor, GNSS, weather, events, energy, network, forecast, routing, anomaly, equity schemas in packages/schemas.
- Digital twin service: in-memory graph (nodes, edges) with state overlay and snapshot API.
- Forecasting service: heuristic baseline congestion forecast; ST-GNN extension point.
- Routing service: multimodal baseline (time, cost, carbon) on twin graph.
- Equity service: district-level Mobility Equity Score from synthetic or file data.
- Anomaly detection: rule-based (incident flags, high occupancy).
- Ingestion pipeline: validation and file-based load from data/samples and data/synthetic.
- Synthetic data: sensor_events, gnss_points, weather, public_events, energy_signals, district_scores in data/synthetic. Seed script scripts/seed_data.py.
- Frontend dashboard: Overview, Network, Forecast, Routing, Equity, Anomalies, Methodology. Vite proxy to API.
- Infrastructure: PostgreSQL schema (infrastructure/db), Dockerfiles for API and web, docker-compose (api, web, postgres, redis). nginx proxy for web container.
- Tests: pytest unit tests (schemas, forecasting, routing, equity, anomaly, ingestion), integration tests (API endpoints via TestClient). Vitest and React Testing Library for frontend.
- Docs: local-development.md, demo-scenario.md, testing.md. Updated README, architecture, api-spec, deployment. Research evaluation-plan aligned with baseline.
- Developer tooling: Makefile (install, run-api, run-web, test, lint, format, typecheck, seed-data), pyproject.toml, package.json, .env.example, .pre-commit-config.yaml.

### Changed

- Repository structure extended with apps/, packages/, services/, infrastructure/, data/. Existing docs and governance preserved and updated.

### Deprecated

- None.

### Removed

- None.

### Fixed

- None.

### Security

- None.

# Implementation status

This document summarizes what is implemented in code versus documented as planned. The repository is the source of truth; this file is a snapshot for onboarding and release.

## Backend (apps/api)

- **Health, version**: Implemented. GET /health, /ready, /version.
- **System**: Implemented. GET /api/v1/system/status, data-sources, data-provenance. Real config and provenance.
- **Alerts**: Implemented. GET /api/v1/alerts, /alerts/{id}. Real transit alert fetchers (BakuBus, Baku Metro official); merge by priority; no fabricated alerts.
- **Weather**: Implemented. GET /api/v1/weather/current, status (Open-Meteo). GET /api/v1/weather/history returns data_status unavailable and empty observations (no persistence).
- **Digital twin**: Implemented. Snapshot, status, coverage, provenance. Real state assembler; no synthetic graph.
- **Network**: Implemented. GET /api/v1/network/graph from twin snapshot.
- **Forecast**: Implemented. Status, models, coverage, features, congestion. Heuristic baseline; FORECAST_ARTIFACT_DIR for registry metadata; learned model (Graph WaveNet/DCRNN) inference path in services/forecasting/inference when artifact and inputs available; API uses baseline when no artifact.
- **Routing**: Implemented. POST /api/v1/routing/plan. Real plan_routes on twin graph; fallback when empty.
- **Equity**: Implemented. GET /api/v1/equity/score. Real when EQUITY_DATA_PATH and district_scores.json; else data_status unavailable.
- **Anomalies**: Implemented. GET /api/v1/anomalies. Rule-based from twin state.
- **Ingestion**: Implemented. POST /api/v1/ingestion/events. Validation only; no persistence.
- **Transit**: Implemented. Providers, routes, stops, network, readiness, GTFS status, alerts, predicted-arrivals, realtime-observations, provider-priority, source-status. Real Baku Metro, BakuBus AYNA, Yandex observed, official alerts.
- **Federated**: Implemented. Status, capabilities, runs, runs/{id}, models, privacy-status. Honest: active False, deployment_mode simulation, runs/models empty, note that artifacts are in services/forecasting/federated.
- **Earth observation**: Implemented. Status, providers, areas, scenes/search, scenes/{id}, layers (true-color, ndvi, ndwi, ndbi), stats (placeholder), provenance. Real Copernicus STAC and Earth Search STAC; EO service on path in main.py.

## Frontend (apps/web)

- **Stack**: Next.js 14.2, React 18, TypeScript. Not Vite.
- **Landing**: Implemented. Hero, Vision, WUF13 sections, Problem, Market context, Urban mobility by the numbers (source-backed facts from lib/facts), Product, How it works, Real data trust, Key modules, Business model, Deployment, Go-to-market, Traction, Competitive landscape, Technology/Data moat, Roadmap, Team, Research, Demo CTA. Images and logos from lib/images.
- **Dashboard**: Implemented. Overview, Digital twin (network), Forecast, Routing, Transit, Equity, Anomalies, Satellite context (EO), Provenance, System status, Methodology. Wired to API where applicable; source-status badges and provenance display.
- **Demo**: Implemented. Demo mode modal and demo page; links to dashboard and product.

## Services

- **transit-ingestion**: Implemented. Registry, BakuBus AYNA, Baku Metro official, official alerts, Yandex observed, merge, GTFS builder, provenance.
- **digital-twin**: Implemented. State assembler; network from PostGIS when configured, weather, no synthetic.
- **forecasting**: Implemented. Pipeline (heuristic baseline), task spec, features, baselines, Graph WaveNet and DCRNN models, inference wrapper, registry, training runner, evaluation. Federated subpackage (Flower direction) with partitioning and task.
- **weather-ingestion**: Implemented. Open-Meteo fetch; used by API.
- **routing**: Implemented. plan_routes on twin graph.
- **equity**: Implemented. get_equity_scores from file when path set.
- **anomaly-detection**: Implemented. Rule-based detector from twin.
- **ingestion**: Implemented. validate_batch; no persistence.
- **network-import**: Implemented. load_network_from_db (PostGIS); used by digital twin when DB enabled.
- **earth-observation**: Implemented. Sentinel-2 STAC search, Copernicus and Earth Search providers, area presets, indices (NDVI, NDWI, NDBI), layer descriptors, caching. AOI stats placeholder.
- **traffic-provider**: On API sys.path; no API router imports it. Not used in active request path.

## Source-status and provenance

- Unified status values (official, public_web_observed, configuration_required, unavailable, etc.) used in schemas and API responses.
- Provenance and data_status on digital twin, weather, transit, EO, equity, forecast. No synthetic substitution in main path.

## Tests

- tests/: API (health, version, network, forecast, routing, equity, anomalies, ingestion, transit, EO, system, weather, alerts), schemas, config, security, digital twin, integration.
- services/forecasting/tests/, services/forecasting/federated/tests/, services/earth-observation/.../tests/: model, baselines, graph, inference, partitioning, EO providers, areas, indices.

## Not implemented or partial

- Weather history persistence: API returns unavailable.
- Federated run/model enumeration: API returns empty; artifacts in service dir.
- EO AOI statistics: Placeholder (status not_computed); real stats require raster pipeline.
- Graph WaveNet/DCRNN in forecast API response: Inference wrapper exists; pipeline uses baseline unless artifact and historical inputs available (see forecasting/inference/wrapper.py).
- traffic-provider: Not wired to any endpoint.

## Documentation

- Architecture, API spec, provider matrix, real-data mode, operational limitations, EO, federated learning, transit integration, and many others in docs/. See README and CHANGELOG for pointers.

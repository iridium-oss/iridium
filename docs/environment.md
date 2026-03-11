# Environment Variables

Environment variables are grouped by subsystem. Copy `.env.example` to `.env` and set values as needed. Do not commit `.env`. This document explains each section, required vs optional usage, and troubleshooting.

## Canonical names

Preferred variables use the `IRIDIUM_` prefix with nested keys and double underscore:

- `IRIDIUM_CORE__ENVIRONMENT`, `IRIDIUM_CORE__API_PORT`
- `IRIDIUM_DB__ENABLED`, `IRIDIUM_DB__DSN`
- `IRIDIUM_CACHE__REDIS_URL`
- `IRIDIUM_PROVIDERS__*`, `IRIDIUM_TRANSIT__*`, `IRIDIUM_EO__*`, `IRIDIUM_TWOGIS__*`, `IRIDIUM_MOOVIT__*`, `IRIDIUM_TELEMETRY__*`, `IRIDIUM_GOMAP__*`

Legacy variables (e.g. `API_PORT`, `POSTGRES_HOST`) remain supported for compatibility but are deprecated for new configuration.

## Section-by-section explanation

### 1. Core application

Controls API bind address, public URL, CORS, logging, and request size. All are optional; defaults allow local development. For production, set `IRIDIUM_CORE__API_BASE_URL` to the public API URL and `IRIDIUM_CORE__CORS_ORIGINS` to allowed frontend origins. Enable `IRIDIUM_CORE__HSTS_ENABLED` only behind TLS.

### 2. Environment and runtime mode

`IRIDIUM_CORE__ENVIRONMENT` (development, staging, production) is optional and used for labeling; no behavior change in current code. Reserved: `DEBUG` for future debug endpoints.

### 3. Frontend (apps/web)

- **NEXT_PUBLIC_API_URL**: Used by client-side fetch in `lib/api.ts` when not using Next.js rewrites. Set to the API URL the browser can reach (e.g. same origin or public API URL).
- **IRIDIUM_API_INTERNAL_URL**: Used by `next.config.js` for server-side rewrites (`/api/*` to API). In Docker, set to `http://api:8000`. Local: `http://localhost:8000`.

Other `NEXT_PUBLIC_*` variables in `.env.example` are reserved for future map defaults and feature toggles.

### 4. Backend API configuration

No additional env is required for Swagger; FastAPI exposes `/docs` by default. `IRIDIUM_API_BASE` is used by scripts (e.g. `measure_api_latency.py`).

### 5. Database

- **IRIDIUM_DB__ENABLED**: Must be `true` to use database-backed network, digital twin graph, or Alembic.
- **IRIDIUM_DB__DSN**: Required when DB is enabled. Use PostgreSQL with PostGIS for network import. Format: `postgresql+psycopg://user:password@host:port/db`.

Services (digital-twin, network-import, Alembic) also read legacy `POSTGRES_*` or `POSTGRES_DSN`. Prefer one consistent set.

### 6. Redis / cache

- **IRIDIUM_CACHE__ENABLED**: Set to `true` to use Redis for caching.
- **IRIDIUM_CACHE__REDIS_URL**: Required when cache is enabled. Example: `redis://localhost:6379/0`. Use password in URL if required; treat as secret if so.

### 7. Logging and observability

- **IRIDIUM_OBSERVABILITY__METRICS_ENABLED**: Enables Prometheus-style metrics when implemented.
- **IRIDIUM_OBSERVABILITY__LOG_HTTP_TIMING**: Logs request timing; default true.

`PROMETHEUS_PORT` and `GRAFANA_URL` are for local or CI observability stack; not read by the API. `SENTRY_DSN` is reserved for error tracking.

### 8. Security and auth

CORS and HSTS are in Core. No session or JWT secrets in current codebase. Add `SECRET_KEY` or `JWT_SECRET` when auth is implemented. `TRUSTED_HOSTS` and `RATE_LIMITING_ENABLED` are reserved.

### 9. Transit and provider flags

- **IRIDIUM_PROVIDERS__OPEN_METEO_ENABLED**, **YANDEX_OBSERVED_ENABLED**, **TWOGIS_ENABLED**, **MOOVIT_ENABLED**: Global toggles. When a provider is enabled, its credentials must be set or startup validation fails (2GIS, Moovit). Transit and weather use these and nested transit/weather settings.

### 10. Azerbaijan-local and transit

Transit aggregation uses AYNA (BakuBus) and Baku Metro static data. AYNA base URLs are hardcoded; no override env in code. BakıKart and iTicket are not implemented; no env. GoMap has settings (`IRIDIUM_GOMAP__API_KEY`, `GOMAP_ALLOWED_SERVER_IP`) but no adapter yet. Transit cache and GTFS output: `IRIDIUM_TRANSIT_CACHE_DIR`, `IRIDIUM_GTFS_OUTPUT_DIR`.

### 11. Weather

Open-Meteo is used by default; no API key. Settings: `IRIDIUM_WEATHER__ENABLED`, `IRIDIUM_WEATHER__PROVIDER_ID`, `IRIDIUM_WEATHER__TIMEOUT_SECONDS`, `IRIDIUM_WEATHER__CACHE_TTL_SECONDS`. Base URL is not overridden via env.

### 12. Earth observation

- **IRIDIUM_EO__ENABLED**: Enable Sentinel-2 endpoints.
- **IRIDIUM_EO__PREFER_COPERNICUS**: Use Copernicus STAC first, then Earth Search.
- **IRIDIUM_EO__SEARCH_CACHE_TTL_SECONDS**: Cache TTL for scene search.

Optional auth: CDSE (username/password or client_id/secret) for higher STAC limits. Sentinel Hub: instance ID and client credentials for Process API when implemented. See `.env.example` and docs/provider-registry.md.

### 13. Routing providers

- **2GIS**: Set `IRIDIUM_TWOGIS__API_KEY` or `TWOGIS_API_KEY`. Used by GET `/api/v1/transit/partner-routes` when key is present. Enable with `IRIDIUM_PROVIDERS__TWOGIS_ENABLED=true` if you want startup validation to require the key.
- **Moovit**: `IRIDIUM_MOOVIT__API_KEY` or `MOOVIT_API_KEY`; interface only; route API not yet implemented.
- **OTP / Valhalla**: Not in API settings; used by routing service when deployed. `OTP_GRAPH_DIR`, `OTP_PORT`, `VALHALLA_URL`.

### 14. Event and venue providers

iTicket and event ingestion are not implemented. See docs/event-sources.md. Variables are reserved.

### 15. Payment and portal

BakıKart is not implemented; no env in code. Reserved for future.

### 16. Telemetry (Traccar)

When **IRIDIUM_TELEMETRY__ENABLED** is true, **IRIDIUM_TELEMETRY__TRACCAR_HOST**, **TRACCAR_USER**, **TRACCAR_PASSWORD** (or legacy `TRACCAR_*`) are required. Consent-based device ingestion only.

### 17. Traffic provider

**TRAFFIC_PROVIDER** and **TRAFFIC_API_KEY** (or **TOMTOM_API_KEY**) are read by the traffic-provider service. When not set, traffic layer returns configuration_required.

### 18. Network import and data paths

**IRIDIUM_NETWORK__ENABLED** and **IRIDIUM_NETWORK__OSM_DATA_DIR** for OSM/PostGIS import. **IRIDIUM_CORE__DATA_SAMPLES_DIR**, **EQUITY_DATA_PATH** (or legacy) for samples and equity data; when equity path is unset, equity API returns unavailable.

### 19. AI / forecasting

**FORECAST_ARTIFACT_DIR**: When set, `/forecast/status` and `/forecast/models` use the artifact directory. No other forecast env is read by current code.

### 20. Federated learning

Federated status is returned by API; no env-driven FL config in code. Reserved for future Flower/server.

### 21. MLOps / artifacts

Only **FORECAST_ARTIFACT_DIR** is in use. Other artifact paths are reserved.

### 22. DevOps / CI

`CI`, `GITHUB_ACTIONS`, `GITHUB_TOKEN`: Set by CI; do not put secrets in `.env`.

### 23. Feature flags and demo mode

No feature-flag env is read by current code; UI is driven by API and provider status. Reserved for future.

### 24. Local development and testing

Reserved for test mocks, skip-external-provider flags, test DB/Redis URLs, and pytest options. See tests/conftest.py for test paths.

### 25. Event streaming

**KAFKA_BOOTSTRAP_SERVERS** is reserved for future event streaming.

---

## Required vs optional matrix

| Context | Required | Optional |
|--------|----------|----------|
| Minimal local API (no DB, no cache) | None | All core; defaults suffice |
| API with database (network, twin) | IRIDIUM_DB__DSN (or POSTGRES_*) when IRIDIUM_DB__ENABLED=true | All core, DB enabled |
| API with Redis cache | IRIDIUM_CACHE__REDIS_URL when IRIDIUM_CACHE__ENABLED=true | All core, cache enabled |
| 2GIS enabled | IRIDIUM_TWOGIS__API_KEY or TWOGIS_API_KEY | IRIDIUM_PROVIDERS__TWOGIS_ENABLED=true |
| Moovit enabled | IRIDIUM_MOOVIT__API_KEY or MOOVIT_API_KEY | IRIDIUM_PROVIDERS__MOOVIT_ENABLED=true |
| Telemetry enabled | TRACCAR_HOST, TRACCAR_USER, TRACCAR_PASSWORD (or IRIDIUM_TELEMETRY__*) | IRIDIUM_TELEMETRY__ENABLED=true |
| Web app (Docker) | IRIDIUM_API_INTERNAL_URL=http://api:8000 | NEXT_PUBLIC_API_URL if client calls API directly |

## Secret vs non-secret matrix

**Secret (do not log or expose):** IRIDIUM_DB__DSN, IRIDIUM_CACHE__REDIS_URL (if with password), POSTGRES_PASSWORD, POSTGRES_DSN, TRACCAR_USER, TRACCAR_PASSWORD, TRAFFIC_API_KEY, IRIDIUM_TWOGIS__API_KEY, IRIDIUM_MOOVIT__API_KEY, IRIDIUM_EO__CDSE_*, IRIDIUM_EO__SENTINEL_HUB_CLIENT_*, IRIDIUM_GOMAP__API_KEY, and legacy equivalents (CDSE_*, SENTINEL_HUB_*, GOMAP_API_KEY, etc.).

**Non-secret:** All core, CORS, ports, URLs (without credentials), feature flags, provider enable flags, paths, log level, observability toggles.

## Local development minimum

- Copy `.env.example` to `.env`.
- Leave IRIDIUM_DB__ENABLED=false and IRIDIUM_CACHE__ENABLED=false unless you run Postgres and Redis.
- Set IRIDIUM_CORE__CORS_ORIGINS to include your frontend origin (e.g. http://localhost:3000).
- For web: IRIDIUM_API_INTERNAL_URL=http://localhost:8000; NEXT_PUBLIC_API_URL=http://localhost:8000 if client-side calls API.

## Recommended demo config

- Same as local minimum.
- Optionally set IRIDIUM_PROVIDERS__TWOGIS_ENABLED=false and IRIDIUM_PROVIDERS__MOOVIT_ENABLED=false (default) so no partner keys are required.
- IRIDIUM_EO__ENABLED=true, IRIDIUM_EO__PREFER_COPERNICUS=true for EO without auth.

## Advanced integration config

- Database: IRIDIUM_DB__ENABLED=true, IRIDIUM_DB__DSN=postgresql+psycopg://...
- Redis: IRIDIUM_CACHE__ENABLED=true, IRIDIUM_CACHE__REDIS_URL=redis://...
- 2GIS: IRIDIUM_PROVIDERS__TWOGIS_ENABLED=true, IRIDIUM_TWOGIS__API_KEY=...
- CDSE auth: IRIDIUM_EO__CDSE_USERNAME and IRIDIUM_EO__CDSE_PASSWORD (or client_id/secret).
- Sentinel Hub: IRIDIUM_EO__SENTINEL_HUB_INSTANCE_ID, IRIDIUM_EO__SENTINEL_HUB_CLIENT_ID, IRIDIUM_EO__SENTINEL_HUB_CLIENT_SECRET.
- Forecast: FORECAST_ARTIFACT_DIR=/path/to/artifact.

## Troubleshooting

- **Startup fails: "2GIS is enabled but IRIDIUM_TWOGIS__API_KEY is not configured"**: Set IRIDIUM_TWOGIS__API_KEY or TWOGIS_API_KEY, or set IRIDIUM_PROVIDERS__TWOGIS_ENABLED=false.
- **Startup fails: "Database is enabled but IRIDIUM_DB__DSN is not configured"**: Set IRIDIUM_DB__DSN (or POSTGRES_DSN) or set IRIDIUM_DB__ENABLED=false.
- **Web cannot reach API**: Ensure IRIDIUM_API_INTERNAL_URL (server-side) and NEXT_PUBLIC_API_URL (client-side, if used) point to the reachable API URL. In Docker, use http://api:8000 for internal.
- **CORS errors**: Add the frontend origin to IRIDIUM_CORE__CORS_ORIGINS (comma-separated, no spaces).
- **Provider shows configuration_required**: Set the required env for that provider (see docs/provider-registry.md) or leave the provider disabled.

## See also

- `.env.example`: Full template with inline comments.
- docs/configuration-reference.md: Table of every variable with purpose, required, secret, default, subsystem.
- docs/provider-registry.md: Provider credentials and legacy env names.
- docs/operational-modes.md: How config affects data_status and behaviour.

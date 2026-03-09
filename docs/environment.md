# Environment Variables

Environment variables are grouped by subsystem. Copy `.env.example` to `.env` and set values as needed. Do not commit `.env`.

## Canonical names

Preferred variables use the `IRIDIUM_` prefix with nested keys:

- `IRIDIUM_CORE__...`
- `IRIDIUM_DB__...`
- `IRIDIUM_CACHE__...`
- `IRIDIUM_PROVIDERS__...`

Legacy variables (for example `API_PORT`) remain supported for compatibility, but should be considered deprecated for new development.

## Environment variable matrix

| Variable | Purpose | Required | Default | Sensitivity |
|----------|---------|----------|---------|-------------|
| IRIDIUM_CORE__ENVIRONMENT | Environment name | No | development | No |
| IRIDIUM_CORE__APP_NAME | Service identifier | No | iridium-api | No |
| IRIDIUM_CORE__APP_VERSION | Service version | No | 0.2.0-dev | No |
| IRIDIUM_CORE__API_HOST | Bind host for API server | No | 0.0.0.0 | No |
| IRIDIUM_CORE__API_PORT | API server port | No | 8000 | No |
| IRIDIUM_CORE__API_BASE_URL | Public base URL for API | No | http://localhost:8000 | No |
| IRIDIUM_CORE__CORS_ORIGINS | Allowed CORS origins (comma-separated) | No | http://localhost:3000,... | No |
| IRIDIUM_CORE__CORS_ALLOW_CREDENTIALS | Allow credentials in CORS | No | false | No |
| IRIDIUM_CORE__CORS_ALLOW_METHODS | Allowed CORS methods (comma-separated) | No | GET,POST,OPTIONS | No |
| IRIDIUM_CORE__CORS_ALLOW_HEADERS | Allowed CORS headers (comma-separated) | No | Authorization,Content-Type,X-Request-ID | No |
| IRIDIUM_CORE__LOG_LEVEL | Logging level | No | INFO | No |
| IRIDIUM_CORE__MAX_REQUEST_BODY_BYTES | Max request body size (Content-Length enforced) | No | 1048576 | No |
| IRIDIUM_CORE__HSTS_ENABLED | Enable Strict-Transport-Security header | No | false | No |
| IRIDIUM_CORE__HSTS_MAX_AGE_SECONDS | HSTS max-age seconds | No | 31536000 | No |
| IRIDIUM_DB__ENABLED | Enable database integration | No | false | No |
| IRIDIUM_DB__DSN | SQLAlchemy DSN for PostgreSQL | When DB enabled | (empty) | Yes |
| IRIDIUM_CACHE__ENABLED | Enable Redis caching | No | false | No |
| IRIDIUM_CACHE__REDIS_URL | Redis connection URL | When cache enabled | (empty) | No |
| IRIDIUM_PROVIDERS__OPEN_METEO_ENABLED | Enable Open-Meteo | No | true | No |
| IRIDIUM_PROVIDERS__YANDEX_OBSERVED_ENABLED | Enable web observed sources | No | true | No |
| IRIDIUM_PROVIDERS__TWOGIS_ENABLED | Enable 2GIS integration | No | false | No |
| IRIDIUM_PROVIDERS__MOOVIT_ENABLED | Enable Moovit integration | No | false | No |
| API_HOST | Bind host for API server | No | 0.0.0.0 | No |
| API_PORT | API server port | No | 8000 | No |
| API_BASE_URL | Public base URL for API | No | http://localhost:8000 | No |
| CORS_ORIGINS | Allowed CORS origins (comma-separated) | No | http://localhost:3000,... | No |
| LOG_LEVEL | Logging level | No | INFO | No |
| APP_VERSION | Application version string | No | 0.2.0-dev | No |
| POSTGRES_HOST | PostgreSQL host | For real network | localhost | No |
| POSTGRES_PORT | PostgreSQL port | No | 5432 | No |
| POSTGRES_USER | PostgreSQL user | No | iridium | No |
| POSTGRES_PASSWORD | PostgreSQL password | No | (empty) | Yes |
| POSTGRES_DB | PostgreSQL database name | No | iridium | No |
| POSTGRES_DSN | Full connection DSN (overrides host/port/user/pass/db) | No | (constructed) | Yes if contains password |
| REDIS_URL | Redis connection URL | No | redis://localhost:6379/0 | No |
| TRAFFIC_PROVIDER | Traffic provider name (e.g. tomtom) | No | tomtom | No |
| TRAFFIC_API_KEY | Traffic provider API key | For live traffic | (empty) | Yes |
| TRACCAR_HOST | Traccar server URL | For telemetry | (empty) | No |
| TRACCAR_USER | Traccar username | No | (empty) | Yes |
| TRACCAR_PASSWORD | Traccar password | No | (empty) | Yes |
| DATA_SAMPLES_DIR | Path to sample data directory | No | data/samples | No |
| EQUITY_DATA_PATH | Path to directory containing district_scores.json | No | (empty) | No |
| OSM_DATA_DIR | Path to OSM raw sources (PBF, manifest) | No | data/manifests/osm | No |
| OTP_GRAPH_DIR | OpenTripPlanner graph directory | For OTP routing | (empty) | No |
| OTP_PORT | OpenTripPlanner service port | No | 8080 | No |
| VALHALLA_URL | Valhalla service URL | For Valhalla routing | (empty) | No |
| KAFKA_BOOTSTRAP_SERVERS | Kafka bootstrap servers | For event streaming | (empty) | No |
| PROMETHEUS_PORT | Prometheus metrics port | No | 9090 | No |
| GRAFANA_URL | Grafana URL | No | (empty) | No |

Sensitivity: **Yes** means the value may contain secrets; do not log or expose in responses. Use optional DOI or arXiv metadata variables only when real identifiers exist.

## Subsystem grouping

- **Core application**: API_HOST, API_PORT, API_BASE_URL, CORS_ORIGINS, LOG_LEVEL, APP_VERSION.
- **Database**: POSTGRES_*.
- **Cache**: REDIS_URL.
- **Routing providers**: OTP_GRAPH_DIR, OTP_PORT, VALHALLA_URL.
- **Traffic providers**: TRAFFIC_PROVIDER, TRAFFIC_API_KEY.
- **Telemetry**: TRACCAR_HOST, TRACCAR_USER, TRACCAR_PASSWORD.
- **Weather**: Open-Meteo is used by default; no key required (see docs/weather-integration.md).
- **Data paths**: DATA_SAMPLES_DIR, EQUITY_DATA_PATH, OSM_DATA_DIR.
- **Event streaming**: KAFKA_BOOTSTRAP_SERVERS.
- **Observability**: PROMETHEUS_PORT, GRAFANA_URL.

## Validation and startup

Required variables depend on operational mode. In public-only mode, only API and optional Postgres (for network) may be needed. In live-data mode, traffic or transit credentials may be required. The application fails explicitly (e.g. data_status configuration_required) when a provider is not configured rather than substituting synthetic data. Startup checks for critical config (e.g. CORS when API is run) are in the application code; see docs/operational-modes.md.

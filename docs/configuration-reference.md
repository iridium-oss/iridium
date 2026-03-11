# Configuration reference

Every environment variable referenced in the repository or in `.env.example`, with purpose, required flag, secret flag, default, subsystem, and notes. Use this as the master reference; see docs/environment.md for section-by-section explanation and troubleshooting.

## Table

| Variable | Purpose | Required | Secret | Default | Subsystem | Notes |
|----------|---------|----------|--------|---------|-----------|-------|
| IRIDIUM_CORE__ENVIRONMENT | Runtime environment name | No | No | development | Backend | development, staging, production |
| IRIDIUM_CORE__APP_NAME | Service identifier | No | No | iridium-api | Backend | |
| IRIDIUM_CORE__APP_VERSION | Version string | No | No | 0.2.0-dev | Backend | |
| IRIDIUM_CORE__API_HOST | API bind host | No | No | 0.0.0.0 | Backend | |
| IRIDIUM_CORE__API_PORT | API server port | No | No | 8000 | Backend | |
| IRIDIUM_CORE__API_BASE_URL | Public API base URL | No | No | http://localhost:8000 | Backend | |
| IRIDIUM_CORE__CORS_ORIGINS | Allowed CORS origins (comma-separated) | No | No | http://localhost:3000,... | Backend | |
| IRIDIUM_CORE__CORS_ALLOW_CREDENTIALS | Allow credentials in CORS | No | No | false | Backend | |
| IRIDIUM_CORE__CORS_ALLOW_METHODS | CORS methods | No | No | GET,POST,OPTIONS | Backend | |
| IRIDIUM_CORE__CORS_ALLOW_HEADERS | CORS headers | No | No | Authorization,Content-Type,X-Request-ID | Backend | |
| IRIDIUM_CORE__LOG_LEVEL | Log level | No | No | INFO | Backend | DEBUG, INFO, WARNING, ERROR |
| IRIDIUM_CORE__MAX_REQUEST_BODY_BYTES | Max request body size | No | No | 1048576 | Backend | |
| IRIDIUM_CORE__HSTS_ENABLED | Enable HSTS header | No | No | false | Backend | Only behind TLS |
| IRIDIUM_CORE__HSTS_MAX_AGE_SECONDS | HSTS max-age | No | No | 31536000 | Backend | |
| IRIDIUM_CORE__DATA_SAMPLES_DIR | Sample data directory | No | No | data/samples | Backend | |
| IRIDIUM_CORE__DATA_SYNTHETIC_DIR | Synthetic data directory | No | No | data/synthetic | Backend | Tests only |
| IRIDIUM_CORE__EQUITY_DATA_PATH | Equity data directory path | No | No | (empty) | Backend | district_scores.json; unset = unavailable |
| API_HOST | Bind host (legacy) | No | No | 0.0.0.0 | Backend | Deprecated |
| API_PORT | API port (legacy) | No | No | 8000 | Backend | Deprecated |
| API_BASE_URL | API base URL (legacy) | No | No | http://localhost:8000 | Backend | Deprecated |
| CORS_ORIGINS | CORS origins (legacy) | No | No | (see core) | Backend | Deprecated |
| LOG_LEVEL | Log level (legacy) | No | No | INFO | Backend | Deprecated |
| APP_VERSION | Version (legacy) | No | No | 0.2.0-dev | Backend | Deprecated |
| NEXT_PUBLIC_API_URL | API URL for client-side fetch | No | No | http://localhost:8000 | Web | lib/api.ts |
| IRIDIUM_API_INTERNAL_URL | API URL for server rewrites | No | No | http://localhost:8000 | Web | next.config.js; Docker: http://api:8000 |
| IRIDIUM_API_BASE | API base for scripts | No | No | http://127.0.0.1:8000 | Scripts | measure_api_latency.py |
| IRIDIUM_DB__ENABLED | Enable database | No | No | false | Backend | |
| IRIDIUM_DB__DSN | PostgreSQL DSN | When DB enabled | Yes | (empty) | Backend | postgresql+psycopg://... |
| POSTGRES_HOST | PostgreSQL host | For real network | No | localhost | Services | digital-twin, network-import, alembic |
| POSTGRES_PORT | PostgreSQL port | No | No | 5432 | Services | |
| POSTGRES_USER | PostgreSQL user | No | No | iridium | Services | |
| POSTGRES_PASSWORD | PostgreSQL password | No | Yes | (empty) | Services | |
| POSTGRES_DB | PostgreSQL database | No | No | iridium | Services | |
| POSTGRES_DSN | Full PostgreSQL DSN | No | Yes | (constructed) | Services | Overrides host/port/user/pass/db |
| IRIDIUM_CACHE__ENABLED | Enable Redis cache | No | No | false | Backend | |
| IRIDIUM_CACHE__REDIS_URL | Redis URL | When cache enabled | If password | (empty) | Backend | redis://... |
| REDIS_URL | Redis URL (legacy) | No | No | redis://localhost:6379/0 | Backend | |
| IRIDIUM_OBSERVABILITY__METRICS_ENABLED | Enable metrics endpoint | No | No | false | Backend | |
| IRIDIUM_OBSERVABILITY__LOG_HTTP_TIMING | Log HTTP timing | No | No | true | Backend | |
| PROMETHEUS_PORT | Prometheus port | No | No | 9090 | DevOps | Not read by API |
| GRAFANA_URL | Grafana URL | No | No | (empty) | DevOps | Not read by API |
| SENTRY_DSN | Sentry DSN | No | Yes | (empty) | Backend | Reserved |
| IRIDIUM_PROVIDERS__OPEN_METEO_ENABLED | Enable Open-Meteo | No | No | true | Backend | |
| IRIDIUM_PROVIDERS__YANDEX_OBSERVED_ENABLED | Enable Yandex observed | No | No | true | Backend | |
| IRIDIUM_PROVIDERS__TWOGIS_ENABLED | Enable 2GIS | No | No | false | Backend | When true, API key required |
| IRIDIUM_PROVIDERS__MOOVIT_ENABLED | Enable Moovit | No | No | false | Backend | When true, API key required |
| IRIDIUM_TRANSIT__ENABLED | Enable transit aggregation | No | No | true | Backend | |
| IRIDIUM_TRANSIT__BAKUBUS_AYNA_ENABLED | Enable AYNA connector | No | No | true | Backend | |
| IRIDIUM_TRANSIT__YANDEX_OBSERVED_ENABLED | Enable Yandex in transit | No | No | true | Backend | |
| IRIDIUM_TRANSIT__CACHE_TTL_SECONDS | Transit cache TTL | No | No | 120 | Backend | |
| IRIDIUM_YANDEX__ENABLED | Yandex observed enabled | No | No | true | Backend | |
| IRIDIUM_YANDEX__DEFAULT_STOP_URL | Default stop URL | No | No | (empty) | Backend | |
| IRIDIUM_YANDEX__TIMEOUT_SECONDS | Yandex request timeout | No | No | 8.0 | Backend | |
| IRIDIUM_TRANSIT_CACHE_DIR | Transit raw cache dir | No | No | .transit_cache | Transit | gitignored |
| IRIDIUM_GTFS_OUTPUT_DIR | GTFS export directory | No | No | feed_export | Transit | |
| IRIDIUM_GOMAP__API_KEY | GoMap API key | No | Yes | (empty) | Backend | Adapter not yet implemented |
| IRIDIUM_GOMAP__BASE_URL | GoMap base URL | No | No | (empty) | Backend | |
| GOMAP_ALLOWED_SERVER_IP | GoMap IP allowlist | No | No | (empty) | Backend | |
| IRIDIUM_WEATHER__ENABLED | Enable weather | No | No | true | Backend | |
| IRIDIUM_WEATHER__PROVIDER_ID | Weather provider id | No | No | open_meteo | Backend | |
| IRIDIUM_WEATHER__TIMEOUT_SECONDS | Weather timeout | No | No | 10.0 | Backend | |
| IRIDIUM_WEATHER__CACHE_TTL_SECONDS | Weather cache TTL | No | No | 300 | Backend | |
| IRIDIUM_EO__ENABLED | Enable EO endpoints | No | No | true | Backend | |
| IRIDIUM_EO__PREFER_COPERNICUS | Prefer Copernicus STAC | No | No | true | Backend | |
| IRIDIUM_EO__COPERNICUS_STAC_URL | Copernicus STAC URL | No | No | (see code) | Backend | |
| IRIDIUM_EO__EARTH_SEARCH_STAC_URL | Earth Search STAC URL | No | No | (see code) | Backend | |
| IRIDIUM_EO__SEARCH_CACHE_TTL_SECONDS | EO search cache TTL | No | No | 300 | Backend | |
| IRIDIUM_EO__CDSE_USERNAME | CDSE username | No | Yes | (empty) | EO | Optional auth |
| IRIDIUM_EO__CDSE_PASSWORD | CDSE password | No | Yes | (empty) | EO | Optional auth |
| IRIDIUM_EO__CDSE_CLIENT_ID | CDSE client id | No | Yes | (empty) | EO | Optional auth |
| IRIDIUM_EO__CDSE_CLIENT_SECRET | CDSE client secret | No | Yes | (empty) | EO | Optional auth |
| CDSE_USERNAME | CDSE username (legacy) | No | Yes | (empty) | EO | |
| CDSE_PASSWORD | CDSE password (legacy) | No | Yes | (empty) | EO | |
| CDSE_CLIENT_ID | CDSE client id (legacy) | No | Yes | (empty) | EO | |
| CDSE_CLIENT_SECRET | CDSE client secret (legacy) | No | Yes | (empty) | EO | |
| IRIDIUM_EO__SENTINEL_HUB_INSTANCE_ID | Sentinel Hub instance ID | No | No | (empty) | EO | Process API |
| IRIDIUM_EO__SENTINEL_HUB_BASE_URL | Sentinel Hub base URL | No | No | (empty) | EO | |
| IRIDIUM_EO__SENTINEL_HUB_CLIENT_ID | Sentinel Hub client id | No | Yes | (empty) | EO | |
| IRIDIUM_EO__SENTINEL_HUB_CLIENT_SECRET | Sentinel Hub client secret | No | Yes | (empty) | EO | |
| SENTINEL_HUB_CLIENT_ID | Sentinel Hub client id (legacy) | No | Yes | (empty) | EO | |
| SENTINEL_HUB_CLIENT_SECRET | Sentinel Hub client secret (legacy) | No | Yes | (empty) | EO | |
| IRIDIUM_TWOGIS__API_KEY | 2GIS API key | When 2GIS enabled | Yes | (empty) | Backend | |
| IRIDIUM_TWOGIS__BASE_URL | 2GIS base URL | No | No | (empty) | Backend | |
| TWOGIS_API_KEY | 2GIS API key (legacy) | No | Yes | (empty) | Transit adapter | |
| IRIDIUM_MOOVIT__API_KEY | Moovit API key | When Moovit enabled | Yes | (empty) | Backend | |
| IRIDIUM_MOOVIT__BASE_URL | Moovit base URL | No | No | (empty) | Backend | |
| MOOVIT_API_KEY | Moovit API key (legacy) | No | Yes | (empty) | Transit adapter | |
| MOOVIT_BASE_URL | Moovit base URL (legacy) | No | No | (empty) | Transit adapter | |
| MOOVIT_PARTNER_API_KEY | Moovit partner key (legacy) | No | Yes | (empty) | Transit adapter | |
| MOOVIT_PARTNER_BASE_URL | Moovit partner URL (legacy) | No | No | (empty) | Transit adapter | |
| OTP_GRAPH_DIR | OTP graph directory | No | No | (empty) | Routing | When OTP used |
| OTP_PORT | OTP service port | No | No | 8080 | Routing | |
| VALHALLA_URL | Valhalla service URL | No | No | (empty) | Routing | |
| IRIDIUM_TELEMETRY__ENABLED | Enable telemetry | No | No | false | Backend | |
| IRIDIUM_TELEMETRY__TRACCAR_HOST | Traccar URL | When telemetry enabled | No | (empty) | Backend | |
| IRIDIUM_TELEMETRY__TRACCAR_USER | Traccar user | When telemetry enabled | Yes | (empty) | Backend | |
| IRIDIUM_TELEMETRY__TRACCAR_PASSWORD | Traccar password | When telemetry enabled | Yes | (empty) | Backend | |
| TRACCAR_HOST | Traccar URL (legacy) | No | No | (empty) | Backend | |
| TRACCAR_USER | Traccar user (legacy) | No | Yes | (empty) | Backend | |
| TRACCAR_PASSWORD | Traccar password (legacy) | No | Yes | (empty) | Backend | |
| TRAFFIC_PROVIDER | Traffic provider name | No | No | tomtom | Traffic | |
| TRAFFIC_API_KEY | Traffic API key | No | Yes | (empty) | Traffic | |
| TOMTOM_API_KEY | TomTom API key | No | Yes | (empty) | Traffic | |
| IRIDIUM_NETWORK__ENABLED | Enable network import | No | No | false | Backend | |
| IRIDIUM_NETWORK__OSM_DATA_DIR | OSM data directory | No | No | data/manifests/osm | Backend | |
| DATA_SAMPLES_DIR | Sample data dir (legacy) | No | No | data/samples | Backend | |
| EQUITY_DATA_PATH | Equity path (legacy) | No | No | (empty) | Backend | |
| OSM_DATA_DIR | OSM dir (legacy) | No | No | data/manifests/osm | Backend | |
| FORECAST_ARTIFACT_DIR | Forecast artifact directory | No | No | (empty) | Backend | /forecast/status, /forecast/models |
| KAFKA_BOOTSTRAP_SERVERS | Kafka bootstrap servers | No | No | (empty) | Event streaming | Reserved |
| CI | CI environment | No | No | (empty) | CI | Set by runner |
| GITHUB_ACTIONS | GitHub Actions | No | No | (empty) | CI | Set by runner |
| USE_MOCK_SERVICES_FOR_TESTS | Use mocks in tests | No | No | (empty) | Tests | Reserved |
| SKIP_EXTERNAL_PROVIDER_TESTS | Skip external provider tests | No | No | (empty) | Tests | Reserved |
| TEST_DATABASE_URL | Test DB URL | No | Yes | (empty) | Tests | Reserved |
| TEST_REDIS_URL | Test Redis URL | No | No | (empty) | Tests | Reserved |
| PYTEST_ADDOPTS | Pytest extra options | No | No | (empty) | Tests | |

## Variables intentionally left out

- **APP_ENV**: Use IRIDIUM_CORE__ENVIRONMENT.
- **WEB_HOST / WEB_PORT**: Not used; Next.js uses its own port.
- **INTERNAL_API_BASE_URL**: Use IRIDIUM_API_INTERNAL_URL for web server-side.
- **ENABLE_SWAGGER**: FastAPI exposes /docs by default; no toggle in code.
- **ENABLE_PROVIDER_HEALTHCHECKS**: Health is on-demand via endpoints; no global disable.
- **ENABLE_BACKGROUND_REFRESH**: No background refresh loop in code.
- **POSTGIS_ENABLED**: PostGIS is assumed when using DB for network; no separate flag.
- **CACHE_TTL_SECONDS / PROVIDER_CACHE_TTL_SECONDS**: Subsystem-specific (weather, transit, EO) have their own TTL vars.
- **SECRET_KEY / JWT_SECRET / SESSION_SECRET**: No session or JWT auth in codebase; add when implemented.
- **ADMIN_EMAIL / SECURITY_CONTACT_EMAIL**: Not read by code.
- **OTEL_* / OTEL_EXPORTER_OTLP_ENDPOINT**: Not wired; reserved.
- **REQUEST_LOGGING_ENABLED / STRUCTURED_LOGGING_ENABLED**: Logging is configured in code; no env toggle.
- **PLAYWRIGHT_BASE_URL**: Not in repo; add to configuration-reference if Playwright tests are added.
- **FEATURE_* / ENABLE_DEMO_MODE**: Not read by code; reserved in .env.example.
- **FEDERATED_* / FLOWER_***: Not read by API; reserved for future FL server.
- **MODEL_ARTIFACT_DIR / DATASET_MANIFEST_DIR / etc.**: Only FORECAST_ARTIFACT_DIR is in use.
- **AYNA_BASE_URL / BAKU_METRO_BASE_URL**: Hardcoded in adapters; override not implemented.
- **BAKIKART_* / ITICKET_***: Integrations not implemented; no env in code.

## Deprecated or legacy

Prefer IRIDIUM_* names. Legacy names are still read for compatibility:

- API_HOST, API_PORT, API_BASE_URL, CORS_ORIGINS, LOG_LEVEL, APP_VERSION
- DATA_SAMPLES_DIR, DATA_SYNTHETIC_DIR, EQUITY_DATA_PATH
- POSTGRES_*, POSTGRES_DSN, REDIS_URL
- TRACCAR_*, TWOGIS_API_KEY, MOOVIT_API_KEY, MOOVIT_PARTNER_*, MOOVIT_BASE_URL
- CDSE_*, SENTINEL_HUB_CLIENT_ID, SENTINEL_HUB_CLIENT_SECRET
- GOMAP_API_KEY, GOMAP_ALLOWED_SERVER_IP

See docs/environment.md and docs/provider-registry.md for propagation and credential fallbacks.

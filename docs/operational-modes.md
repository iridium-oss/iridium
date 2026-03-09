# Operational Modes

IRIDIUM can be run in several operational modes depending on available data sources and credentials.

## Mode summary

| Mode | Description | Credentials required | Intended use |
|------|--------------|----------------------|--------------|
| Public-only | OSM network (if loaded), Open-Meteo weather. No traffic or transit feeds. | None for basic run; Postgres for network. | Local dev, judges without keys. |
| Public-data | As above plus optional equity data from EQUITY_DATA_PATH and recorded snapshots if present. | None or file paths. | Demo with recorded real snapshots. |
| Live-data | Traffic and/or transit and/or telemetry when configured. | TRAFFIC_API_KEY and/or GTFS/operator access, TRACCAR_* as needed. | Internal demo, pilot. |
| Full observability | Stack with Prometheus, Grafana. | Optional. | Dev and staging. |

## Startup and Makefile targets

| Target | Purpose |
|--------|---------|
| run-core | Start API and web locally (make run-api, make run-web in two terminals). |
| run-public-data | Same as core; use with public-only env (no traffic/transit keys). |
| run-live-data | Docker with profiles for live integrations, or local with .env set for traffic/transit. |
| run-demo | Stack suitable for demo (docker compose up or run-api + run-web). |
| run-observability | Docker with with-observability profile (Prometheus). |
| stop-stack | docker compose down. |
| reset-local | docker compose down -v; clears Postgres data. Use with care. |

- **Local**: `make run-api`, `make run-web`. Uses .env; data status is explicit when sources are missing. Best for active development.
- **Docker**: Use compose profiles (see docs/docker-profiles.md). `docker compose --profile core up -d` runs core (api, web, postgres, redis).

## Failure behaviour

When a provider is unavailable or not configured, the API returns data_status (unavailable, configuration_required, permission_required) and does not substitute synthetic data. See docs/real-data-mode.md and docs/failure-fallbacks.md.

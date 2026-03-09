# Observability

IRIDIUM provides a minimal observability baseline intended for local development and future extension.

## Logs

- API logs are structured JSON.
- Each request is assigned a correlation id via `X-Request-ID`.

## Metrics

The repository includes a Prometheus configuration at `infrastructure/observability/prometheus/prometheus.yml`.
Prometheus is started via Docker Compose profile `with-observability`.

Start:

- `docker compose --profile core --profile with-observability up -d`

Prometheus:

- `http://localhost:9090`

Notes:

- Prometheus is configured to scrape `/metrics` from the API if it is exposed.
- Metrics must reflect real behavior and must not imply coverage that is not implemented.

## Health surfaces

- `/health` for liveness
- `/ready` for readiness

Provider health is exposed via dedicated API endpoints. Provider availability must remain truthful and explicit.


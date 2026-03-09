# Docker Compose Profiles

The stack uses Compose profiles to enable optional services. Add `--profile <name>` to enable a profile.

## Profile matrix

| Profile | Included services | Intended use | Credentials |
|---------|-------------------|--------------|-------------|
| core | api, web, postgres, redis | Default. Local dev and demo. | Optional: .env overrides. |
| public-data | core with public providers enabled | Public-only operation without partner keys. | None. |
| live-data | core with live integrations enabled by config | Local run when credentials exist. | Provider credentials. |
| with-observability | core + prometheus | Metrics collection for dev. | None. |
| with_routing | (placeholder) | OTP or Valhalla when added. | OTP_GRAPH_DIR or VALHALLA_URL as needed. |
| with_scheduler | (placeholder) | Airflow or cron when added. | As per scheduler docs. |

## Intended audience

| Audience | Recommended profile | Notes |
|----------|---------------------|--------|
| Judges / reviewers | core | Public-only data; no traffic/transit keys required. |
| Developers | core, optionally with_observability | Full local stack; add profiles as needed. |
| Demo with live data | core; set .env for traffic/transit if available | See docs/live-demo-runbook.md. |
| CI | core or none | Use only what tests need. |

## Commands

- `docker compose --profile core up -d`: Starts core (api, web, postgres, redis).
- `docker compose --profile public-data up -d`: Starts public-data mode.
- `docker compose --profile live-data up -d`: Starts live-data mode (requires credentials).
- `docker compose --profile core --profile with-observability up -d`: Adds Prometheus.
- `docker compose down`: Stops all. Use `-v` to remove volumes (resets Postgres data).

See docs/operational-modes.md for operational modes and docs/live-demo-operations.md for demo guidance.

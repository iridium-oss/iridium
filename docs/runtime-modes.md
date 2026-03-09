# Runtime modes

IRIDIUM supports multiple runtime modes. Modes are defined by configuration, not by code branches that fabricate data.

## core

Purpose: Local development stack with API, web, Postgres, Redis.

Start:

- `docker compose --profile core up -d`

Notes:

- Postgres is available for future persistence and network import workflows.
- The API must still expose `data_status` fields per endpoint when required inputs are missing.

## public-data

Purpose: Run with public sources only and no partner credentials.

Start:

- `docker compose --profile public-data up -d`

Notes:

- Public web observed sources are allowed, but must be labeled as such.
- If a partner integration is not configured, the API must return `configuration_required` or `permission_required` as appropriate.

## live-data

Purpose: Enable live integrations when credentials and permissions are available.

Start:

- `docker compose --profile live-data up -d`

Notes:

- Live mode does not imply that all providers are available.
- Provider availability must be exposed via source status fields and system endpoints.

## with-observability

Purpose: Add a minimal observability stack for local inspection.

Start:

- `docker compose --profile core --profile with-observability up -d`

Notes:

- Prometheus is configured to scrape `/metrics` from the API if it is exposed.
- Do not claim metrics coverage beyond what is actually implemented.


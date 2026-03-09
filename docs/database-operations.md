# Database operations

IRIDIUM uses PostgreSQL 16 for persistence. PostGIS is planned for spatial queries and network import workflows.

## Local database via Docker Compose

Start database:

- `docker compose --profile core up -d postgres`

Default credentials are for local development only and are defined in `docker-compose.yml`.

## Migrations

Alembic configuration:

- `alembic.ini`
- `infrastructure/db/alembic/`

Run migrations:

- `make db-migrate`

Create a new migration:

- `alembic revision -m "message"`

## Reset

Developer-safe destructive reset:

- `make db-reset`

This removes volumes. It is intended for local development only.


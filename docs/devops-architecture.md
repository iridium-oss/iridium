# DevOps architecture

This document describes the local development and CI foundation for IRIDIUM.

## Local stack

Primary orchestration uses Docker Compose:

- `api` (FastAPI)
- `web` (static build served by nginx)
- `postgres` (PostgreSQL 16)
- `redis` (Redis 7)
- `prometheus` (optional, profile `with-observability`)

Profiles are documented in `docs/runtime-modes.md`.

## Environment variables

Canonical environment variables use `IRIDIUM_` prefix with nested keys.
See `docs/environment.md`.

## Database operations

Database schema initialization exists via `infrastructure/db/schema.sql`.
Migrations are added when the persistence layer is enabled.

## CI principles

- Reproducibility over speed.
- No implicit network dependencies in tests.
- Truthful reporting of provider availability and data status.


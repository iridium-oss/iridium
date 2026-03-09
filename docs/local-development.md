# Local Development

This document describes how to run IRIDIUM locally for development and demos.
The baseline test suite uses synthetic fixtures, but the platform is designed to operate on real or recorded data when configured.

## Prerequisites

- Python 3.12+
- Node.js 18+
- (Optional) Docker and Docker Compose for full stack

## One-time setup

1. Clone the repository and open a terminal at the repo root.

2. Create a virtual environment and install Python dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -e ./packages/schemas
   pip install -e ".[dev]"     # root pyproject
   pip install -e ./apps/api
   ```

3. Seed or verify synthetic data:
   ```bash
   python scripts/seed_data.py
   ```
   This uses `data/synthetic` and optionally runs the ingestion pipeline. No persistence is required for the baseline.

4. Frontend (one-time install, then dev):
   ```bash
   cd apps/web && npm ci
   npm run dev
   ```
   First run: `npm ci` or `npm install` installs dependencies (once). Then `npm run dev` starts the dev server with Turbopack at http://localhost:3000 (fast startup). The app proxies `/api`, `/health`, and `/version` to the API. Scripts use `npx next` so the dev server runs correctly on Windows even when `node_modules/.bin` is not on PATH.

   **Windows:** If `npm install` fails with EPERM or ENOTEMPTY, close all terminals and IDEs using the repo, then remove `apps/web/node_modules` and `apps/web/.next` and run `npm install` again from `apps/web`.

## Running the API

From the repo root (with the same virtual environment activated):

```bash
cd apps/api && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or use the Makefile:

```bash
make run-api
```

The API will be at http://localhost:8000. OpenAPI docs: http://localhost:8000/docs.

## Running the frontend

```bash
make run-web
```

Or:

```bash
cd apps/web && npm run dev
```

Ensure the API is running so that dashboard views can load data.

## Running tests

- Python (unit and integration):
  ```bash
  pytest tests/ -v
  ```

- Frontend:
  ```bash
  cd apps/web && npm run test
  ```

- Lint and format:
  ```bash
  make lint
  make format
  make typecheck
  ```

## Docker Compose

To run the full stack (API, web, PostgreSQL, Redis) in containers:

```bash
docker compose --profile core up -d
```

- API: http://localhost:8000
- Web: http://localhost:3000 (Next.js; API proxied to the api service)
- PostgreSQL: localhost:5432 (user iridium, password iridium, db iridium)
- Redis: localhost:6379

The API container currently uses in-memory state; it does not require the database to be up for the baseline. The database schema in `infrastructure/db/schema.sql` is applied on first start for future use.

## Environment variables

Copy `.env.example` to `.env` and adjust if needed. Key variables:

- `CORS_ORIGINS`: Allowed origins for the API (default includes http://localhost:3000).
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR.
- `DATA_SAMPLES_DIR`, `DATA_SYNTHETIC_DIR`: Paths for sample and synthetic data (relative to repo root when running from root).

## What is implemented vs planned

- **Implemented**: API with health, version, network graph, forecast, routing, equity, anomalies, ingestion (validate-only); in-memory digital twin; baseline forecasting and routing; synthetic data and seed script; frontend dashboard; Docker and Compose; pytest and frontend tests.
- **Planned**: Persistence (PostgreSQL), streaming ingestion, ST-GNN forecasting, federated learning, full schedule-based routing, PostGIS. See ROADMAP.md.

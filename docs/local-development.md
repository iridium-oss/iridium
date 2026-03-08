# Local Development

This document describes how to run IRIDIUM locally for development and demos. All data used is synthetic; no real city or user data is required.

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

4. Frontend (separate terminal):
   ```bash
   cd apps/web && npm ci && npm run dev
   ```
   The Vite dev server runs at http://localhost:3000 and proxies `/api`, `/health`, and `/version` to the API.

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
  cd apps/web && npm run test:run
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
docker compose up -d
```

- API: http://localhost:8000
- Web: http://localhost:3000 (nginx serves the built app and proxies API requests to the api service)
- PostgreSQL: localhost:5432 (user iridium, password iridium, db iridium)
- Redis: localhost:6379

The API container currently uses in-memory state; it does not require the database to be up for the baseline. The database schema in `infrastructure/db/schema.sql` is applied on first start for future use.

## Environment variables

Copy `.env.example` to `.env` and adjust if needed. Key variables:

- `CORS_ORIGINS`: Allowed origins for the API (default includes http://localhost:3000).
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR.
- `DATA_SAMPLES_DIR`, `DATA_SYNTHETIC_DIR`: Paths for sample and synthetic data (relative to repo root when running from root).

## What is implemented vs planned

- **Implemented**: API with health, version, network graph, forecast, routing, equity, anomalies, ingestion (validate-only); in-memory digital twin; baseline forecasting and routing; synthetic data and seed script; frontend dashboard; Docker and Compose; pytest and Vitest tests.
- **Planned**: Persistence (PostgreSQL), streaming ingestion, ST-GNN forecasting, federated learning, full schedule-based routing, PostGIS. See ROADMAP.md.

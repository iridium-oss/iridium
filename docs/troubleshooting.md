# Troubleshooting

Common issues when running IRIDIUM locally and how to resolve them.

## API does not start

- **ModuleNotFoundError for iridium_schemas or digital_twin**: Install packages and add service paths. From repo root run: `pip install -e ./packages/schemas` and ensure you start the API from `apps/api` with the repo root on PYTHONPATH, or use `make run-api` which runs from the correct directory. The API main.py adds service paths automatically when run from repo root.
- **Port 8000 in use**: Change API_PORT in .env or run uvicorn with a different port: `uvicorn app.main:app --port 8001`.
- **CORS errors in browser**: Ensure CORS_ORIGINS in .env includes your frontend origin (e.g. http://localhost:3000). Restart the API after changing .env.

## Frontend cannot reach API

- **Network error or "API unreachable"**: Start the API first (make run-api). The Vite dev server proxies /api, /health, and /version to localhost:8000; ensure the proxy target in vite.config.ts matches your API host and port.
- **404 on /api/v1/...**: The proxy forwards paths as-is. Check that the API is listening on the same port as in the proxy config (default 8000).

## Tests fail

- **ImportError in pytest**: Run pytest from the repository root so that sys.path and package discovery work. Install deps: `pip install -e ./packages/schemas` and optionally install services as editable if you have changed them.
- **Integration test fails (test_api_health)**: The integration tests use FastAPI TestClient and mount the app. They do not require a running server. If imports fail, ensure apps/api is on PYTHONPATH when running from repo root (e.g. `python -m pytest tests/`).
- **Frontend tests**: Run from apps/web with `npm run test:run`. Ensure dependencies are installed with `npm ci`.

## Seed or synthetic data

- **No data in views**: Run `python scripts/seed_data.py` from repo root. Synthetic data lives in data/synthetic/. If the equity service loads district_scores.json, ensure that file exists (it is committed in the repo).
- **Ingestion returns validation errors**: The ingestion endpoint validates batch structure. Ensure sensor_events, gnss_points, etc. match the schemas in packages/schemas (e.g. timestamp, segment_id, speed_kmh within range).

## Docker

- **Build fails for API**: The Dockerfile copies packages/schemas and services into the image. Build from repo root: `docker compose build api`. Ensure all COPY paths exist.
- **Web container cannot reach API**: In docker-compose, the web service uses hostname `api` to proxy. Ensure the api service is healthy (healthcheck) and that nginx.conf proxies to `http://api:8000`.

## General

- **Broken links in docs**: Links are relative to the docs/ folder. From README use paths like docs/architecture.md.
- **Pre-commit hook fails**: Run `pre-commit run --all-files` to see which check fails. Common: trailing whitespace, missing newline at EOF, or the no-emdash check (remove any em dash or en dash from modified files).

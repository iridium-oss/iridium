# Testing

This document describes the test strategy and how to run tests for IRIDIUM.

## Python tests

Tests live under `tests/`. The test runner is pytest. Run from the repo root:

```bash
pytest tests/ -v
```

### Unit tests

- **test_schemas.py**: Pydantic schema validation (sensor events, route request, forecast segment, equity, anomaly). Ensures contracts accept valid data and reject invalid data.
- **test_forecasting.py**: Forecasting pipeline; horizon, segment list, and segment field ranges.
- **test_routing.py**: Routing service; response shape and alternative segments.
- **test_equity.py**: Equity score computation; default districts and composite score range.
- **test_anomaly.py**: Anomaly detector; list shape, since filter, and required fields.
- **test_ingestion.py**: Ingestion batch validation and run_ingestion with synthetic dirs.

### Integration tests

- **tests/integration/test_api_health.py**: FastAPI TestClient against the full app. Covers GET /health, /version, /api/v1/network/graph, /api/v1/forecast/congestion, POST /api/v1/routing/plan, GET /api/v1/equity/score, GET /api/v1/anomalies, POST /api/v1/ingestion/events. No live server required; the client mounts the app.

To run only integration tests:

```bash
pytest tests/integration/ -v
```

### Test data

Unit and integration tests use the in-memory digital twin and synthetic data under `data/synthetic/`. No database or external services are required for the baseline suite.

## Frontend tests

Frontend tests use Vitest and React Testing Library. Run from the repo root or from apps/web:

```bash
cd apps/web && npm run test:run
```

Current coverage includes a smoke test for the App (layout and navigation). Additional component or API-boundary tests can be added under `apps/web/src`.

## Coverage

Coverage is measured over `apps`, `packages`, and `services`. Install `pytest-cov` (e.g. `pip install pytest-cov` or use the `dev` extra), then run:

```bash
pytest tests/ --cov=apps --cov=packages --cov=services --cov-report=term-missing --cov-report=html
```

- **term-missing**: prints missing line numbers per file.
- **html**: writes `htmlcov/` for a browser report.

Configuration lives in `pyproject.toml` under `[tool.coverage.run]` and `[tool.coverage.report]`. The build is configured with `fail_under = 100`; use `# pragma: no cover` on defensive or hard-to-test branches (e.g. HTTP error returns, optional imports) so that the main paths stay covered and the report reaches 100%.

- **Warnings**: Deprecation warnings for `datetime.utcnow()` are suppressed via `filterwarnings` in `[tool.pytest.ini_options]`; production code uses `datetime.now(timezone.utc)`.
- **Exclude lines**: `exclude_lines` in coverage skip `pragma: no cover`, `def __repr__`, `raise NotImplementedError`, `if TYPE_CHECKING:`, `if __name__ == "__main__":`, and `except ImportError:` so optional or CLI-only code does not lower the percentage.

## CI

GitHub Actions run lint and tests as defined in `.github/workflows/ci.yml`. The workflow runs pytest and, if present, frontend tests. Ensure all tests pass before merging.

## What is not tested

- End-to-end browser tests (e.g. Playwright) are not included in the baseline.
- Performance and load tests are not included.
- Federated learning and ST-GNN code paths are not yet implemented; tests will be added when those components exist.

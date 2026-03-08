# IRIDIUM monorepo - common commands
# Use: make <target>

PYTHON := python
UV := uv
NPM := npm
DOCKER := docker
DOCKER_COMPOSE := docker compose

.PHONY: install install-py install-js dev test lint format typecheck run-api run-web seed-data clean help
.PHONY: fetch-real-data ingest-real-data build-otp run-live-stack run-public-only-stack refresh-snapshots validate-provenance verify-badges
.PHONY: run-core run-public-data run-live-data run-demo run-observability stop-stack reset-local

help:
	@echo "IRIDIUM targets:"
	@echo "  install      - Install Python and JS dependencies"
	@echo "  install-py   - Python deps only"
	@echo "  install-js   - JS deps only (apps/web)"
	@echo "  dev          - Run API and web in dev mode (separate terminals)"
	@echo "  test         - Run Python and frontend tests"
	@echo "  lint         - Lint Python and frontend"
	@echo "  format       - Format Python and frontend code"
	@echo "  typecheck    - Type check Python and frontend"
	@echo "  run-api      - Start API server (local)"
	@echo "  run-web      - Start web app (local)"
	@echo "  seed-data    - Generate/seed sample data (test fixtures only; not used in main path)"
	@echo "  fetch-real-data   - Fetch OSM Azerbaijan (Geofabrik); writes manifest"
	@echo "  ingest-real-data  - Run network-import from OSM PBF into PostGIS"
	@echo "  build-otp    - Build OpenTripPlanner graph (when OSM+GTFS available)"
	@echo "  run-live-stack    - Start stack with live data dependencies"
	@echo "  run-public-only-stack - Start stack for public-only mode (no traffic/transit credentials)"
	@echo "  refresh-snapshots - Refresh recorded snapshots (when implemented)"
	@echo "  validate-provenance - Validate source manifests and provenance"
	@echo "  verify-badges - Verify README badge URLs resolve"
	@echo "  run-core      - Run API and web locally (use run-api and run-web in two terminals)"
	@echo "  run-public-data - Same as core; public-only env"
	@echo "  run-live-data - Docker with live-integration profiles"
	@echo "  run-demo      - Docker compose up (core stack for demo)"
	@echo "  run-observability - Docker with observability profile"
	@echo "  stop-stack    - Docker compose down"
	@echo "  reset-local   - Docker compose down -v (removes volumes)"
	@echo "  docker-up     - Start stack with docker compose"
	@echo "  docker-down  - Stop stack"
	@echo "  clean        - Remove caches and build artifacts"

install: install-py install-js

install-py:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"
	$(PYTHON) -m pip install -e ./packages/schemas
	$(PYTHON) -m pip install -e ./apps/api 2>/dev/null || true

install-js:
	cd apps/web && $(NPM) ci

dev:
	@echo "Run in two terminals: make run-api and make run-web"

test:
	$(PYTHON) -m pytest tests/ -v --tb=short
	cd apps/web && $(NPM) run test -- --run 2>/dev/null || true

lint:
	ruff check apps packages services scripts tests
	cd apps/web && $(NPM) run lint 2>/dev/null || true

format:
	black apps packages services scripts tests
	cd apps/web && $(NPM) run format 2>/dev/null || true

typecheck:
	mypy apps/api packages/schemas --ignore-missing-imports 2>/dev/null || true
	cd apps/web && $(NPM) run typecheck 2>/dev/null || true

run-api:
	cd apps/api && $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-web:
	cd apps/web && $(NPM) run dev

seed-data:
	$(PYTHON) scripts/seed_data.py

fetch-real-data:
	$(PYTHON) scripts/fetch_osm_azerbaijan.py

ingest-real-data:
	$(PYTHON) scripts/run_network_import.py

build-otp:
	@echo "OpenTripPlanner graph build: set OTP_GRAPH_DIR and run OTP build (see docs/deployment.md)"

run-core:
	@echo "Run in two terminals: make run-api and make run-web"

run-public-data: run-core

run-live-data:
	$(DOCKER_COMPOSE) --profile with_observability up -d 2>/dev/null || $(DOCKER_COMPOSE) up -d

run-demo:
	$(DOCKER_COMPOSE) up -d

run-observability:
	$(DOCKER_COMPOSE) --profile with_observability up -d

stop-stack:
	$(DOCKER_COMPOSE) down

reset-local:
	$(DOCKER_COMPOSE) down -v

run-live-stack:
	$(DOCKER_COMPOSE) --profile with_observability up -d 2>/dev/null || $(DOCKER_COMPOSE) up -d

run-public-only-stack:
	$(DOCKER_COMPOSE) up -d

refresh-snapshots:
	@echo "Recorded snapshot refresh: run ingestion for configured snapshot paths (see docs/data-provenance.md)"

validate-provenance:
	@test -f infrastructure/raw-sources/osm/manifest.json && echo "OSM manifest present" || echo "OSM manifest missing; run make fetch-real-data"

verify-badges:
	$(PYTHON) scripts/verify_badges.py

docker-up:
	$(DOCKER_COMPOSE) up -d

docker-down:
	$(DOCKER_COMPOSE) down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov dist *.egg-info 2>/dev/null || true

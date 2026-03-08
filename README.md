# IRIDIUM

[![License: EUPL-1.2](https://img.shields.io/badge/License-EUPL--1.2-blue.svg)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
[![CI](https://github.com/iridium-oss/iridium/actions/workflows/ci.yml/badge.svg)](https://github.com/iridium-oss/iridium/actions/workflows/ci.yml)
[![Lint](https://github.com/iridium-oss/iridium/actions/workflows/lint.yml/badge.svg)](https://github.com/iridium-oss/iridium/actions/workflows/lint.yml)
[![Docs](https://github.com/iridium-oss/iridium/actions/workflows/docs.yml/badge.svg)](https://github.com/iridium-oss/iridium/actions/workflows/docs.yml)
[![GitHub issues](https://img.shields.io/github/issues/iridium-oss/iridium)](https://github.com/iridium-oss/iridium/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/iridium-oss/iridium)](https://github.com/iridium-oss/iridium/pulls)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18915211.svg)](https://doi.org/10.5281/zenodo.18915211)
[![arXiv](https://img.shields.io/badge/arXiv-submit/7340933-B31B1B.svg)](https://arxiv.org/abs/submit/7340933)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=white)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.4-336699?style=flat&logo=postgis&logoColor=white)](https://postgis.net/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Ruff](https://img.shields.io/badge/Ruff-Linter-FCC21B?style=flat&logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![ESLint](https://img.shields.io/badge/ESLint-Checked-4B32C3?style=flat&logo=eslint&logoColor=white)](https://eslint.org/)
[![Prettier](https://img.shields.io/badge/Prettier-Formatted-F7B93E?style=flat&logo=prettier&logoColor=white)](https://prettier.io/)

---

IRIDIUM is a real-time urban mobility prediction and optimization platform for Azerbaijani cities. It is designed around federated machine learning, a dynamic digital twin of the transport network, and four core modules: congestion forecasting, multimodal adaptive routing, Mobility Equity Score, and anomaly detection with dynamic rerouting. The platform is intended to support privacy-preserving and regulation-aware deployment; raw personal data does not leave local nodes.

**Status**: Real-data mode. When sources are configured, the platform uses OSM network data, Open-Meteo weather, and optional traffic/transit/telemetry. When not configured, API and UI show explicit status (unavailable, configuration_required). No synthetic data in the main runtime path. See [docs/real-data-mode.md](docs/real-data-mode.md) and [docs/operational-limitations.md](docs/operational-limitations.md). Federated learning and ST-GNN forecasting are planned; see [ROADMAP.md](ROADMAP.md).

## Summary

- **Problem**: Urban mobility faces congestion, inequitable access, and data fragmentation. Combining data for prediction and optimization often conflicts with privacy and data sovereignty.
- **Approach**: Federated learning (data stays local; only model updates are shared), a digital twin (graph of network and state), and modular services for forecast, routing, equity, and anomalies.
- **Current implementation**: FastAPI backend, digital twin state assembler (real sources only), heuristic forecast, baseline routing, equity from configured data, rule-based anomaly detection, ingestion validation, React dashboard. Data is real or recorded when configured; otherwise status is explicit. Synthetic data is only in isolated test fixtures.
- **Audience**: Transport planners, researchers, hackathon judges, and future open source contributors.

## Quick start

Prerequisites: Python 3.12+, Node.js 18+.

```bash
git clone https://github.com/iridium-oss/iridium.git && cd iridium
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ./packages/schemas && pip install -e ".[dev]" && pip install -e ./apps/api
make run-api    # Terminal 1: API at http://localhost:8000
make run-web    # Terminal 2: Dashboard at http://localhost:3000
```

Optional: for real network data, run `make fetch-real-data`, then install and run network-import (see [docs/data-provenance.md](docs/data-provenance.md)). Optional: `make seed-data` for test fixtures only (not used in main path).

Open http://localhost:3000 for the dashboard; http://localhost:8000/docs for the API. Full setup: [docs/local-development.md](docs/local-development.md). Demo: [docs/demo-scenario.md](docs/demo-scenario.md). Testing: [docs/testing.md](docs/testing.md). Issues: [docs/troubleshooting.md](docs/troubleshooting.md).

## What is implemented

| Component | Status |
|-----------|--------|
| Backend API | FastAPI; health, version, network, forecast, routing, equity, anomalies, ingestion. |
| Digital twin | State assembler merges real sources (OSM/PostGIS, weather, traffic); nodes, edges, provenance. |
| Congestion forecast | Heuristic baseline; ST-GNN extension point. |
| Multimodal routing | Time, cost, carbon on twin graph; baseline optimizer. |
| Mobility Equity Score | District-level indicators from EQUITY_DATA_PATH when set; otherwise data_status unavailable. |
| Anomaly detection | Rule-based (incident flags, high occupancy). |
| Ingestion | Validation and file-based load; no central raw-data store. |
| Frontend | React + TypeScript dashboard; all modules. |
| Federated learning | Not implemented; architecture and docs only. |
| Persistence | PostgreSQL schema provided; API uses in-memory state. |

## Architecture

- **Local training nodes** (planned): Data stays on participant sites; training produces model updates.
- **Encrypted parameter aggregation** (planned): Central or distributed aggregation of model updates only.
- **Digital twin**: Graph of nodes (segments, junctions, stops) and edges with time-varying state; fed by ingestion (sensors, weather, events).
- **APIs**: Forecast, routing, equity, anomalies consumed by the dashboard and external systems.

Details: [docs/architecture.md](docs/architecture.md), [docs/system-overview.md](docs/system-overview.md). Federated learning and core modules: [docs/federated-learning.md](docs/federated-learning.md).

## Operational modes

| Mode | Services | Credentials | Use |
|------|----------|-------------|-----|
| Public-only | API, web, optional Postgres | None | Judges, local dev |
| Public-data | As above; EQUITY_DATA_PATH, recorded snapshots optional | None or paths | Demo with recorded data |
| Live-data | Traffic, transit, telemetry when configured | API keys, operator access | Pilot, internal demo |
| Observability | Prometheus (optional profile) | None | Dev, staging |

See [docs/operational-modes.md](docs/operational-modes.md) and [docs/docker-profiles.md](docs/docker-profiles.md).

## Data source summary

| Source | Access | Status in baseline |
|--------|--------|---------------------|
| OSM (Geofabrik) | Public | Fetch + network-import into PostGIS |
| Open-Meteo | Public | Live when reachable |
| Baku Metro / BakuBus | Permission required | Registry only until feed provided |
| Traffic (e.g. TomTom) | API key | configuration_required when unset |
| Traccar | Optional | Unavailable until configured |
| Equity | File path | Unavailable when EQUITY_DATA_PATH unset |

See [docs/provider-matrix.md](docs/provider-matrix.md) and [docs/real-data-mode.md](docs/real-data-mode.md).

## Mathematical framing

Routing minimises a weighted objective over travel time, cost, emissions, and penalties:

$$
J(r) = \alpha \, T(r) + \beta \, C(r) + \gamma \, E(r) + \delta \, P(r)
$$

where $T(r)$ is travel time, $C(r)$ cost, $E(r)$ emissions proxy, and $P(r)$ transfer or accessibility penalty. Federated learning aggregates local updates (e.g. FedAvg-style): global parameters $\theta^{(t+1)} = \sum_{k=1}^{K} \frac{n_k}{\sum_j n_j} \theta_k^{(t)}$ where $n_k$ is local sample count at client $k$. Forecasting targets short-horizon state on graph $G=(V,E)$ with input $X_{t-T+1:t}$ and forecast $\hat{Y}_{t+1:t+H} = f_\theta(X_{t-T+1:t}, G)$. Equity composite for district $d$: $MES_d = \sum_m w_m z_{d,m}$ with normalised indicators $z_{d,m}$. See [docs/symbol-glossary.md](docs/symbol-glossary.md) and [docs/math-style-guide.md](docs/math-style-guide.md).

## Scholarly artifacts

| Artifact | Status |
|----------|--------|
| CITATION.cff | Present at repo root; use for citation. |
| Zenodo DOI | Published; see [https://doi.org/10.5281/zenodo.18915211](https://doi.org/10.5281/zenodo.18915211). |
| arXiv preprint | Under submission; see [submit/7340933](https://arxiv.org/abs/submit/7340933). |

Citation: [docs/citation.md](docs/citation.md).

## Academic paper

A full manuscript package is in [paper/](paper/):
```
O. Y. Laitinen Imanov et al. (2026). "IRIDIUM: A Provenance-Aware Urban Mobility Platform for Digital Twin Assembly, Multimodal Analytics, and Federated Learning in Azerbaijani Cities." arXiv:submit/7340933. DOI: 10.5281/zenodo.18915211 (Released March 8, 2026).
```
 IEEE journal LaTeX (IEEEtran); prepared for arXiv and journal submission. Contents: real-data architecture, digital twin, formalization of routing, forecasting, equity, anomaly, and FedAvg, and baseline evaluation (API semantics, data-status, latency, weather integration). Build and figure instructions: [paper/README.md](paper/README.md). arXiv: run `python paper/scripts/package_arxiv.py` to produce [paper/arxiv/](paper/arxiv/) source zip. No arXiv identifier is claimed until the preprint is submitted.

## Repository map

```
apps/api          FastAPI application
apps/web          React dashboard (Vite)
packages/schemas  Pydantic data contracts
services/         ingestion, digital-twin, forecasting, routing, equity, anomaly-detection
infrastructure/   db schema, Dockerfiles
data/synthetic    Test fixtures only; not used in main runtime path
docs/             Architecture, API spec, local dev, demo, reviewer guide, product scope
research/         Problem statement, methodology, evaluation, risks
```

## Demo and review

- **Demo**: [docs/demo-scenario.md](docs/demo-scenario.md) (3-5 minute walkthrough).
- **Judges and reviewers**: [docs/reviewer-guide.md](docs/reviewer-guide.md), [docs/product-scope.md](docs/product-scope.md), [docs/one-page-summary.md](docs/one-page-summary.md).

## Real data and baseline

The main runtime path uses real or recorded data when configured (OSM network, Open-Meteo weather, optional traffic/transit). When a source is not configured, the API returns explicit data_status (unavailable, configuration_required, permission_required). Synthetic data is not used in the main path; it may exist only in isolated test fixtures. See [docs/real-data-mode.md](docs/real-data-mode.md), [docs/provider-matrix.md](docs/provider-matrix.md), and [docs/operational-limitations.md](docs/operational-limitations.md). The platform does not claim production readiness or regulatory compliance.

## Future work

Federated learning orchestration, ST-GNN congestion forecasting, PostgreSQL persistence for the twin, full schedule-based routing, and streaming ingestion are planned. See [ROADMAP.md](ROADMAP.md) and [docs/technical-decisions.md](docs/technical-decisions.md).

## Team

| Name | Role |
|------|------|
| Olaf Yunus Laitinen Imanov | AI Engineer |
| Amina Sadiqzade | Frontend Developer |
| Malahat Ismayilova | AI Engineer |
| Aslan Ibadullayev | Frontend Developer |
| Fidan Bagirova | AI Engineer |

[GOVERNANCE.md](GOVERNANCE.md) defines maintainer roles and decision-making.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, commit messages, pull requests, and coding standards. All contributions must follow the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Use formal, professional language; no emojis; no em dash or en dash in text.

## License

This project is licensed under the European Union Public Licence v. 1.2 only (EUPL-1.2). See [LICENSE](LICENSE).

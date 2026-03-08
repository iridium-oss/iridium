# IRIDIUM - One-Page Summary

**Project**: IRIDIUM - Real-time urban mobility prediction and optimization platform for Azerbaijani cities.

**Track**: Data, AI and Digital Urban Mobility.

**Problem**: Urban mobility faces congestion, inequitable access, and data fragmentation. Centralising mobility data raises privacy and regulatory concerns. IRIDIUM addresses this with a federated learning architecture and a modular platform: forecasting, multimodal routing, Mobility Equity Score, and anomaly detection.

**Architecture**: (1) Local training nodes keep raw data on-site. (2) Only encrypted or privacy-preserving model updates are shared with an aggregation service. (3) A digital twin (graph of network and state) is updated from heterogeneous sources (sensors, weather, events). (4) APIs expose forecast, routing, equity, and anomalies to a technical dashboard.

**Implemented baseline**: FastAPI backend with health, version, network graph, congestion forecast (heuristic), multimodal route planning (time/cost/carbon), district-level Mobility Equity Score, rule-based anomaly detection, and ingestion validation. React dashboard for all modules. In-memory digital twin; synthetic data only. Docker Compose for local stack.

**Planned**: Federated learning orchestration, ST-GNN congestion forecasting, PostgreSQL persistence, full schedule-based routing, streaming ingestion.

**Why federated learning**: Design choice to support privacy-preserving and regulation-aware deployment. No centralisation of raw personal data. Does not guarantee legal compliance; deployers conduct their own assessment.

**Why synthetic data**: Public repository contains no real city or user data. Enables evaluation and extension without operational data; real data is a deployment concern.

**Team**: Olaf Yunus Laitinen Imanov, Amina Sadiqzade, Malahat Ismayilova, Aslan Ibadullayev, Fidan Bagirova.

**Run locally**: `make run-api` and `make run-web`; see docs/local-development.md. Demo path: docs/demo-scenario.md.

**License**: EUPL-1.2 only.

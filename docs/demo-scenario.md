# Demo Scenario

Structured walkthrough for demonstrating IRIDIUM at a hackathon or technical review. All data is synthetic; the system is a baseline implementation. This document provides a 3-5 minute user journey and concrete narrative scenarios.

## Prerequisites

1. Start the API: `make run-api` (or `cd apps/api && python -m uvicorn app.main:app --reload`).
2. Start the frontend: `make run-web` (or `cd apps/web && npm run dev`).
3. Optionally run `make seed-data` to confirm synthetic data.
4. Open http://localhost:3000 in a browser.

## Recommended Demo Sequence (3-5 minutes)

| Step | View | Action | What to say |
|------|------|--------|-------------|
| 1 | Overview | Land on dashboard; show health and version. | "IRIDIUM is an urban mobility platform. The API is up; all data you see is synthetic." |
| 2 | Network | Open Network. Show nodes and edges table. | "The digital twin is a graph of the transport network. In production this would be fed by sensors and ingestion; here it is in-memory." |
| 3 | Forecast | Open Forecast. Show congestion segments. | "We forecast congestion over the next two hours. This uses a heuristic baseline; the architecture is ready for an ST-GNN model." |
| 4 | Routing | Open Routing. Use defaults; click Plan route. Show alternatives. | "Routing supports time, cost, and carbon. This is a baseline optimizer on the demo graph." |
| 5 | Equity | Open Equity. Show district scores. | "The Mobility Equity Score highlights district-level accessibility. It is for policy discussion; limitations are documented." |
| 6 | Anomalies | Open Anomalies. | "Anomalies are rule-based today: incidents and high occupancy. List may be empty if the twin has no flags." |
| 7 | Methodology | Open Methodology. | "Here we summarise what is implemented versus planned: federated learning, ST-GNN, and persistence are next." |

## Narrative Scenarios (for context only; data remains synthetic)

These scenarios describe the kind of situations the platform is designed to support. They are not backed by real data in the repository.

- **Morning congestion build-up**: The forecast view shows how congestion could evolve over the next 2-3 hours. The baseline uses current twin state and a simple decay; a future ST-GNN would use historical patterns.
- **Major public event surge**: Synthetic public events exist in `data/synthetic/public_events.json`. The anomaly detector can flag demand-surge proxies (e.g. high occupancy); event-driven logic is a planned extension.
- **Temporary road closure**: The digital twin supports an incident flag on edges. The routing service avoids incident edges when computing routes. Demonstrating this would require setting an incident on an edge in the twin (code or future UI).
- **District-level accessibility disparity**: The Equity view shows different composite scores and indicators per district. Central has higher accessibility proxies than South in the default synthetic data; this illustrates how the score can surface gaps.

## What Is Implemented Versus Simulated

- **Implemented**: API, digital twin graph, heuristic forecast, baseline routing, equity score from file/synthetic data, rule-based anomalies, ingestion validation, frontend wired to API.
- **Simulated**: All data (sensors, weather, events, districts) is synthetic. No real city or user data.
- **Planned**: Federated learning, ST-GNN, persistence, full journey planner, streaming ingestion.

## If Live Services Fail

- Have the API and frontend running locally before the demo.
- If the API is down, the Overview will show an error; explain that the backend is required and restart it.
- Screenshots of key views (Network, Forecast, Routing, Equity) can be used as fallback; document them in a folder or in this doc if the team prepares them.
- OpenAPI at http://localhost:8000/docs can be used to show and call endpoints directly.

## Presenter Checklist

- [ ] API and web are running; Overview shows "Status: ok".
- [ ] Tabs or navigation ready: Overview, Network, Forecast, Routing, Equity, Anomalies, Methodology.
- [ ] Default routing origin/destination pre-filled; one click to "Plan route".
- [ ] Emphasise: baseline implementation, synthetic data, privacy-by-design, no production claims.
- [ ] Point judges to docs/reviewer-guide.md and docs/product-scope.md for quick orientation.

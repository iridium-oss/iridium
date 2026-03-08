# Live Demo Runbook

Use this runbook when running a live demo (e.g. for judges or reviewers).

## Recommended demo mode

- **Judges**: Use **public-only** mode. Start with `make run-demo` (Docker) or `make run-api` and `make run-web` in two terminals. No traffic or transit credentials required. Data shown will be: Open-Meteo weather (if reachable), empty or OSM-loaded network (if you ran fetch-real-data and network-import), and explicit status for unconfigured sources. See docs/demo-checklist.md.

## Pre-demo checklist

- [ ] API and web start successfully.
- [ ] Health endpoint returns 200: `curl -s http://localhost:8000/health`.
- [ ] Dashboard loads at http://localhost:3000.
- [ ] Know which panels will show "live" vs "unavailable" or "configuration required" (see docs/provider-matrix.md).
- [ ] If using Docker, ensure postgres has schema (volume or init). For network graph, run fetch-real-data and network-import beforehand or accept empty graph.

## Critical paths and fallbacks

| Demo step | Primary | Fallback if unavailable |
|-----------|---------|-------------------------|
| Show dashboard | All panels load | Explain data_status per panel (live / unavailable / configuration required). |
| Network graph | Loaded from PostGIS if available | Show empty graph and note "Run OSM fetch and network-import to load." |
| Forecast | Heuristic from twin state | Show response with data_status; explain baseline. |
| Routing | Plan route with current twin | If graph empty, result may be minimal; explain. |
| Equity | Scores if EQUITY_DATA_PATH set | Show "unavailable" and point to docs/fairness.md. |
| Anomalies | List from real inputs if any | Show empty list or rule-based examples; explain. |

See docs/failure-fallbacks.md and docs/presenter-flow.md for narrative and failure handling.

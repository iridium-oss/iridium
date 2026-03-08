# Live Demo Operations

Operational guidance for running a live demo with real or recorded data.

## Which demo mode for judging

Use **public-only** mode: no traffic or transit API keys required. Start the stack with `make run-demo` or `make run-api` and `make run-web`. The dashboard will show:

- **Live**: Open-Meteo weather (if reachable).
- **Unavailable or configuration required**: Network (unless OSM import was run), traffic, transit, equity (unless EQUITY_DATA_PATH set), and optionally anomalies depending on inputs.

Judges see honest data status on each panel. See docs/live-demo-runbook.md and docs/demo-checklist.md.

## Prefer real data or recorded snapshots

When credentials and access exist, use live data. When not, use **recorded real snapshots** with provenance (source, captured_at, redaction status) if legally stored; otherwise do not show synthetic data and show "unavailable" or "configuration required." See docs/real-data-mode.md and docs/data-provenance.md.

## Fallbacks

If a provider is rate-limited, credentials fail, network is down, or routing backend is unavailable, the application returns explicit data_status and does not fabricate data. See docs/failure-fallbacks.md and docs/incident-playbook.md for response behaviour and presenter narrative.

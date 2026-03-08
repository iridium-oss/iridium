# Failure Fallbacks

How the platform behaves when a provider or service fails. No synthetic data is substituted in the main path.

## Demo critical paths and fallback screens

| Scenario | What the user sees | Presenter action |
|----------|--------------------|------------------|
| Weather API down or rate-limited | data_status: unavailable; empty or last weather | "Weather source is temporarily unavailable; we do not show fabricated data." |
| Traffic not configured | data_status: configuration_required | "Traffic requires an API key; see docs for how to enable it." |
| Transit not configured | data_status: permission_required | "Transit feeds require operator agreement; Baku Metro and BakuBus are documented." |
| Network not loaded | Empty graph; data_status configuration_required or unavailable | "Run OSM fetch and network-import to load the road network." |
| Equity data path not set | Empty districts; data_status unavailable | "Equity uses real or recorded district data; set EQUITY_DATA_PATH to enable." |
| API unreachable | Frontend error or timeout | Restart API; check CORS and port; see docs/incident-playbook.md. |
| Routing backend (OTP/Valhalla) not deployed | Baseline routing on twin only | "We use the digital twin for baseline routing; OTP/Valhalla can be added when the graph is built." |

## Operator narrative

- Be explicit: "This value is live," "This is unavailable because credentials are not set," or "This is a recorded real snapshot from [date]."
- Do not claim production readiness or that all sources are live when they are not. Point to docs/operational-limitations.md when asked about gaps.

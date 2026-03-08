# Demo Checklist

Use before and during a live demo.

## Before demo

| Step | Done |
|------|------|
| Environment: .env present (or use defaults); no secrets in slides or screen. | |
| API: make run-api or Docker api healthy. | |
| Web: make run-web or Docker web serving. | |
| Health: curl http://localhost:8000/health returns 200. | |
| Provider matrix reviewed: know which sources are live vs unconfigured. | |
| Fallback narrative ready: what to say when a panel shows unavailable (see docs/presenter-flow.md). | |

## During demo

| Step | Done |
|------|------|
| Open dashboard; show Overview and system status. | |
| Show Network (graph or empty with data_status). | |
| Show Forecast (heuristic; data_status in response). | |
| Show Routing (plan a route; note data_status). | |
| Show Equity and Anomalies; explain when data is unavailable. | |
| If something fails: state the failure and fallback (docs/incident-playbook.md). | |

## After demo

| Step | Done |
|------|------|
| Stop stack if needed (make stop-stack or Ctrl+C). | |
| Do not leave .env or credentials on shared machines. | |

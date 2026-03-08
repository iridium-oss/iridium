# Incident Playbook

Operational response for common failure modes. Use when running a demo or when supporting users.

## Provider or API failure

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Weather panel shows unavailable | Open-Meteo rate limit or network | Retry later; check LOG_LEVEL. No synthetic fallback. |
| Traffic panel shows configuration_required | TRAFFIC_API_KEY unset or invalid | Set key or present as "traffic not configured" in demo. |
| Transit shows permission_required | No GTFS feed configured | Expected until operator provides feed; see docs/operator-integration-requirements.md. |
| Network graph empty | Postgres not populated or not connected | Run make fetch-real-data, then network-import; set POSTGRES_* and apply schema. |
| Equity returns empty districts | EQUITY_DATA_PATH unset or path missing | Set path to directory with district_scores.json or present as "equity data not configured." |

## API or frontend down

| Symptom | Action |
|---------|--------|
| API health fails | Restart API; check CORS and port. Check logs for missing imports (e.g. service paths). |
| Frontend cannot reach API | Verify API_BASE_URL and CORS_ORIGINS; ensure API is running. |
| 500 on forecast or network | Check digital twin and state assembler; ensure optional deps (weather_ingestion, traffic_provider) are on path or errors handled. |

## Data and provenance

- Do not enable synthetic data in the main path to "fix" missing providers. Keep data_status honest.
- If a demo must run without a provider, use the documented fallback message (e.g. "configuration required") and point to docs/operational-limitations.md.

## Escalation

For security or data breach concerns, follow your organisation's incident process. The repository does not store personal data; any such data would be in deployer-controlled systems (e.g. Traccar, operator feeds).

# Provider Refresh Matrix

Per-provider refresh, timeout, retry, and fallback behaviour. Align with docs/ingestion-schedules.md and docs/data-refresh-policy.md.

| Source | Provider | Cadence | Timeout | Retry | Cache TTL | Stale threshold | Fallback |
|--------|----------|---------|---------|-------|-----------|-----------------|----------|
| Network | Geofabrik OSM | On demand / daily | 600s | 1 | N/A | N/A | Empty graph; configuration_required |
| Weather | Open-Meteo | Hourly | 30s | 2 | 1 h | 2 h | unavailable |
| Transit | Baku Metro / BakuBus | When feed available | 120s | 2 | 24 h | 24 h | permission_required |
| Traffic | TomTom or other | 10 min | 20s | 2 | 10 min | 15 min | configuration_required |
| Telemetry | Traccar | Near real time | 15s | 2 | 5 min | 10 min | unavailable |
| Events | iTicket / CityLife | 6-12 h | 60s | 1 | 6 h | 12 h | unavailable |
| Energy | As per docs/energy-context | Low frequency | 60s | 1 | 24 h | 48 h | unavailable |

When Airflow or another scheduler is implemented, DAGs or jobs should follow these values. Document any changes in this file and in ingestion-schedules.md.

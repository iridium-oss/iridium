# Ingestion Schedules

When ingestion is automated (e.g. via cron or Airflow), use the following schedule and policy guidance. The repository does not yet ship a scheduler; this document defines the intended cadence and behaviour.

## Target refresh frequency

| Source family | Target frequency | Cron expression (example) | Timeout | Retry |
|---------------|------------------|----------------------------|---------|--------|
| Weather (Open-Meteo) | Hourly | `0 * * * *` | 30s | 2 |
| OSM network | On demand or daily | Manual or `0 2 * * *` | 600s | 1 |
| Transit (GTFS static) | Daily or when operator publishes | `0 4 * * *` or on webhook | 120s | 2 |
| Traffic (provider API) | Every 5-15 min when configured | `*/10 * * * *` | 20s | 2 |
| Event ingestion | Every 6-12 h | `0 */6 * * *` | 60s | 1 |
| Snapshot materialisation | Every 15-30 min if used | `*/15 * * * *` | 120s | 1 |

Cron expressions are in the format: minute hour day month weekday. Adjust for timezone and deployment.

## Stale thresholds

| Source | Stale threshold | Behaviour when stale |
|--------|-----------------|----------------------|
| Weather | 2 h | Mark data_status stale; continue serving last. |
| Traffic | 15 min | Mark stale; routing may use last or fall back. |
| Transit | 24 h (static) | Alert; do not mark live. |
| Network (OSM) | N/A (static until re-import) | No automatic refresh. |

See docs/data-refresh-policy.md and docs/provider-refresh-matrix.md for cache TTL and fallback behaviour.

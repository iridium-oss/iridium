# Data Refresh Policy

Policies for refreshing and invalidating data from external sources.

## Cache TTL and refresh

| Source | Cache TTL | Refresh trigger | Fallback when unavailable |
|--------|-----------|-----------------|---------------------------|
| Weather | 1 h | Scheduled or on request | Return unavailable; no synthetic. |
| Traffic | 10-15 min | Scheduled or on request | Return configuration_required or unavailable. |
| Transit (static) | 24 h | Scheduled or manual | Return permission_required or unavailable. |
| Network (PostGIS) | N/A | Loaded at startup or on demand from DB | Empty graph + configuration_required if not loaded. |
| Equity | N/A | File-based; reload on request or restart | Unavailable if EQUITY_DATA_PATH not set. |

## Timeout and retry

- **Timeout**: Each provider request should have a timeout (e.g. 20-30 s for APIs). On timeout, mark that source as unavailable for this cycle and log.
- **Retry**: One or two retries with backoff for transient failures. Do not retry indefinitely; after failure, set data_status to unavailable and surface in API/UI.
- **Rate limiting**: Respect provider rate limits (e.g. Open-Meteo). Back off when 429 or equivalent is returned; document in docs/provider-refresh-matrix.md.

## Observability

- Log refresh success and failure per source; do not log sensitive payloads.
- Optionally expose a metric or health endpoint per source (e.g. last_success_timestamp). See observability docs when implemented.

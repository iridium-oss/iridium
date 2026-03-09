# Data Quality and Drift

This document describes data quality signals, freshness, and degradation behavior in IRIDIUM. It supports operational trust in the AI layer.

## Source Quality and Freshness

- **Digital twin**: data_status and source_provenance on the snapshot indicate per-source status and fetched_at. No aggregate quality score is computed yet; consumers use data_status (live, unavailable, configuration_required) and provenance to judge.
- **Forecast**: source_coverage in the response (e.g. twin_edges=N) and data_status from the twin. No freshness threshold is enforced; the baseline uses the latest assembled snapshot.
- **Equity**: data_status and source_coverage (e.g. districts count). When no data path is set, data_status is unavailable.
- **Routing**: data_status on the response; when the graph is empty, data_status is unavailable or configuration_required.

## Missingness

- No active AI endpoint fills missing data with synthetic values. Missing or unavailable data leads to empty results, reduced coverage, or explicit fallback with metadata (e.g. fallback_used, confidence_note).
- Equity: missing file or path yields empty districts. Forecast: zero edges still produce baseline segments with a note. Anomaly: only edges in the snapshot are scanned.

## Staleness and Invalidation

- Snapshot is assembled on demand (or per request) from state_assembler. There is no explicit TTL or staleness threshold in the baseline; deployment can add caching with invalidation if needed.
- Stale output is not silently reused as "live"; data_status reflects the state at response time.

## Drift and Degradation

- **Drift detection**: Not implemented in the baseline. Future work may add drift indicators (e.g. distribution shift on key features) and document them here.
- **Unstable-model suppression**: N/A for current deterministic baselines. When a learned model is added, suppression or fallback to baseline on high uncertainty or low confidence can be added.
- **Explicit degraded mode**: Forecast, routing, and equity all return structured metadata (model_type, data_status, confidence_note, fallback_used) so that clients can treat responses as degraded when appropriate.

## Provider Confidence

- Source provenance includes status per provider. If a provider repeatedly fails or returns invalid data, the provenance note can reflect it; no automatic confidence downgrading is implemented yet. This is a candidate for future quality-control logic.

## Alerting

- No built-in alerting for low-quality model conditions. Deployment can add monitoring on data_status, fallback_used, or source_provenance and surface alerts via existing observability (logging, metrics).

This layer keeps the AI outputs honest and interpretable under missing or degraded data.

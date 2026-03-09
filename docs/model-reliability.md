# Model Reliability and Serving

This document describes how AI and scoring outputs are served with consistent metadata, how confidence and degradation are communicated, and how production baselines are distinguished from experimental logic.

## Metadata on Every AI Output

Every major AI or scoring response includes (where applicable):

- **model_type**: deterministic_baseline | statistical_baseline | ml_baseline | rule_baseline | experimental
- **model_maturity**: production_baseline | experimental | inactive
- **data_status**: live | unavailable | configuration_required | recorded_real_snapshot
- **source_coverage**: Short summary of upstream data (e.g. twin_edges, district count)
- **confidence_note**: Explanation of confidence or uncertainty; for baselines, states that there is no calibrated uncertainty
- **fallback_used**: True if a degraded or fallback path was used

## Subsystem Semantics

| Subsystem | model_type | Meaning of confidence_note |
|-----------|------------|----------------------------|
| Forecast | deterministic_baseline | Heuristic has no calibrated uncertainty; use for operational awareness only. |
| Anomaly | rule_baseline | Rule-based; confidence not computed. |
| Equity | deterministic_baseline | Composite from file-based proxies; interpret with caution when coverage is partial. |
| Routing | deterministic_baseline | Weighted path on real graph; fallback_used when no path found. |

Confidence is not equated with correctness. Each subsystem documents what its outputs represent and under what data conditions they are valid.

## Degraded and Fallback Behavior

- **Forecast**: Always returns heuristic baseline; no silent switch to synthetic data. data_status reflects twin state.
- **Anomaly**: Uses assembled snapshot only; no fabricated anomalies.
- **Equity**: When no data path is configured, returns empty districts and data_status unavailable with a clear note.
- **Routing**: When no path exists in the graph, returns a single fallback segment with description explaining "No path found; fallback estimate only" and fallback_used True. No fake optimal route.

## Model Version and Artifact Linkage

Production baseline models do not load external artifacts; they are code-defined. When a learned model is introduced, every response must reference model version, dataset version, and training config where applicable. Experimental models must not be served as production_baseline.

## Latency and Validation

AI endpoints must complete within acceptable bounds. Request validation (e.g. horizon limits, segment count limits) is applied. On failure, the API returns a structured error or a truthful degraded response with metadata, not a fabricated success.

See [ai-capability-audit.md](ai-capability-audit.md) for what is production vs experimental.

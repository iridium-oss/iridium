# AI, Statistics, and Systems Finalization Report

This report summarizes the work done to bring IRIDIUM's AI-related and mathematically grounded layers to a production-grade state. No fabricated data, model accuracy, or deployment status was added. All changes preserve honest degradation and traceability.

---

## 1. AI Functions Finalized

**Forecasting**
- Production path is heuristic baseline only. No ST-GNN or learned model in runtime.
- Response includes model_type (deterministic_baseline), model_maturity (production_baseline), source_coverage (e.g. twin_edges=N), confidence_note (no calibrated uncertainty), fallback_used (False). data_status from twin.
- Pipeline uses get_assembled_snapshot(); no synthetic runtime data.

**Anomaly detection**
- Rule-based only: incident flag and occupancy > 85%. source_type (observed_disruption | inferred_statistical) and evidence_summary on each event.
- Detector uses get_assembled_snapshot() for consistency with forecast and routing. Deduplication by anomaly_id; since filter for staleness.
- API response includes model_type, model_maturity, data_status, note.

**Equity**
- File-based district_scores.json only; composite = (pt + modal + aff) / 3. When no data, returns empty districts and data_status unavailable with clear note.
- Response includes model_type, model_maturity, source_coverage, confidence_note.

**Routing**
- Uses get_assembled_snapshot(). Weighted objective (time, cost, carbon) formalized in code and docs. When no path found, returns single fallback segment with description "No path found; fallback estimate only" and fallback_used True. Response includes model_type, model_maturity, data_status, fallback_used.

---

## 2. Statistical Foundations Finalized

- **Descriptive**: Equity composite is explicit average of three proxies; no synthetic defaults in main path.
- **Missing data**: No active AI endpoint fills gaps with synthetic data; missing data leads to unavailable or explicit fallback with metadata.
- **Uncertainty**: confidence_note on forecast and equity states baseline has no calibrated uncertainty; interpret with caution.
- **Documentation**: docs/statistical-methods.md describes policy and per-subsystem behavior.

---

## 3. Optimization and Calculus Logic Finalized

- **Routing objective**: Documented in docs/optimization-and-objectives.md. Formula: time 1.0*d + 0.1*c + 0.5*k; cost 0.2*d + 2.0*c + 0.1*k; carbon 0.1*d + 0.2*c + 5.0*k. Implemented in routing/plan.py _weight().
- **Multi-objective**: Single scalar combination; weights fixed in code. No arbitrary client-supplied weights.

---

## 4. CS and Algorithmic Improvements

- **Data source consistency**: Forecast, anomaly, and routing all use get_assembled_snapshot() so the same data path and provenance apply.
- **Routing**: Empty graph returns structured response with data_status; path search uses same snapshot. Fallback is explicit and labeled.
- **No silent fallbacks**: Placeholder route only when no path exists; description and fallback_used make it clear.

---

## 5. Fake or Weak AI Paths Removed or Clarified

- No synthetic runtime substitution in forecast, anomaly, equity, or routing.
- Routing fallback text changed from "Baseline placeholder route" to "No path found; fallback estimate only. Load network for real routing." and fallback_used set True.
- ST-GNN and federated learning documented as not active in runtime (ai-capability-audit.md, federated-learning-status.md).

---

## 6. Model Governance and Serving

- **Schemas**: Forecast, anomaly, equity, and routing responses include model_type, model_maturity, and where applicable data_status, source_coverage, confidence_note, fallback_used.
- **Maturity**: All active paths use production_baseline. Experimental and future work are documented as such.
- **Version**: model_version (e.g. baseline-heuristic) and generated_at/requested_at on responses.

---

## 7. Evaluation and Tests

- **Tests**: test_congestion_forecast_metadata checks model_type, model_maturity, fallback_used, confidence_note. test_plan_routes_response_metadata checks model_type, model_maturity, fallback_used, data_status. test_plan_routes_no_path_fallback updated for new fallback description and fallback_used True.
- **Routing tests**: All use get_assembled_snapshot (patched). Anomaly tests use get_assembled_snapshot (patched).
- No fake benchmarks or placeholder metrics added. Evaluation of a future learned model will be documented separately.

---

## 8. API and Frontend Contracts

- **Backend**: Pydantic schemas extended with model_type, model_maturity, source_coverage, confidence_note, fallback_used, data_status where applicable. Anomaly events have optional confidence, source_type, evidence_summary.
- **Frontend**: apps/web/lib/api.ts updated so CongestionForecast, RouteResponse, AnomaliesResponse, and EquityScore include the new optional metadata fields for dashboard and consumers.

---

## 9. Documentation Added or Updated

| Document | Purpose |
|----------|---------|
| docs/ai-capability-audit.md | Classification of every AI function: production-ready, baseline-only, scaffolded, concept/future. Source of truth for scope. |
| docs/forecasting.md | Problem definition, production baseline, interfaces, no ST-GNN in runtime. |
| docs/model-reliability.md | Metadata on every AI output, confidence semantics, degraded and fallback behavior. |
| docs/optimization-and-objectives.md | Routing objective formula and coefficients; consistency with code. |
| docs/statistical-methods.md | Descriptive stats, missing data policy, uncertainty, no false precision. |
| docs/equity-analytics.md | Composite formula, data source, bias notes, API metadata. |
| docs/anomaly-detection.md | Current implementation: rule-based only; source_type and evidence_summary; z-score future. |
| docs/data-quality-and-drift.md | Source quality, freshness, missingness, staleness, degraded mode. |
| docs/federated-learning-status.md | FL not active; positioning as research pathway only. |
| docs/ai-architecture.md | Summary of production components, data-to-model pipeline, governance. |
| docs/model-serving.md | API contracts, validation, failure and degradation. |

---

## 10. AI Functions Intentionally Left Experimental or Inactive

- **ST-GNN forecasting**: Documented in modeling.md; not in runtime. Not presented as production.
- **Statistical anomaly (z-score, rolling baseline)**: Documented in anomaly-detection.md; not in runtime.
- **Federated learning**: Documented in federated-learning.md and federated-learning-status.md; not active. Product and API do not present FL as production.
- **ETA / arrival prediction**: Not implemented; not claimed.
- **Forecast uncertainty bands**: Baseline has no calibrated uncertainty; confidence_note explains this.

---

## Summary

IRIDIUM's AI, statistics, calculus, and core CS layers are now in a production-grade state: real data only in the main path, explicit metadata on every AI output, formalized routing objective, consistent use of the assembled snapshot, honest fallback behavior, and clear separation between production baselines and future/experimental work in code and documentation.

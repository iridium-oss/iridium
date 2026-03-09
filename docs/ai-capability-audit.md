# AI Capability Audit

This document classifies all AI-related functionality in IRIDIUM by implementation status. Only truthful and working AI functionality remains active in the main runtime path. Experimental or future work is explicitly marked.

## Classification Legend

- **Production-ready**: Implemented, traceable to real data or deterministic baseline, documented, and safe for serving.
- **Baseline-only**: Implemented with rule-based or heuristic logic; no learned model; suitable as production baseline.
- **Scaffolded**: Code or API exists but not yet reliable; must not be presented as production.
- **Concept / future**: Documented as intended design; not active in current runtime.
- **Removed or deactivated**: Fake or weak logic removed from main path or explicitly degraded.

---

## Congestion Forecasting

| Item | Status | Notes |
|------|--------|------|
| Heuristic baseline from twin edges | Baseline-only | Uses assembled snapshot edges; decay-based projection. No learned model. |
| ST-GNN or learned forecast | Concept / future | Documented in modeling.md; not in runtime. Do not present as production. |
| Forecast metadata (horizon, model_version, data_status) | Production-ready | Response includes generated_at, model_version, data_status, note. |
| Prediction horizon, segment targeting | Production-ready | horizon_minutes (1 to 180); optional segment_ids. |
| Uncertainty or confidence band | Baseline-only | Not yet exposed; baseline has no calibrated uncertainty. |

**Scope**: Active production path is heuristic baseline only. All forecast responses carry model_version and data_status so consumers can distinguish baseline from future learned models.

---

## Multimodal Routing Intelligence

| Item | Status | Notes |
|------|--------|------|
| Weighted objective (time, cost, carbon) | Baseline-only | Formula in routing/plan.py; configurable via optimize parameter. |
| Graph-based pathfinding (DFS) | Baseline-only | Works on real twin graph when loaded; no Dijkstra yet; may be slow on large graphs. |
| Fallback when no path | Production-ready | Returns single placeholder segment with explicit note; response indicates fallback. |
| Transfer count, segment breakdown | Production-ready | Returned in RouteAlternative. |
| Real-time disruption weighting | Concept / future | Anomaly flags can be used to update twin; reroute is "recompute with current twin." |

**Scope**: Production path uses real graph when available; fallback is explicit and labeled. Optimization objective is documented and implemented consistently.

---

## ETA or Arrival Prediction

| Item | Status | Notes |
|------|--------|------|
| Transit ETA / predicted arrival | Concept / future | Not implemented. API and docs must not claim it as current. |

---

## Anomaly Detection

| Item | Status | Notes |
|------|--------|------|
| Rule-based (incident flag, occupancy > 85%) | Baseline-only | Uses twin edges; incident and demand_surge types. |
| Severity, type, segment_ids, detected_at | Production-ready | AnomalyEvent schema and detector output. |
| Z-score or statistical deviation | Concept / future | Documented in anomaly-detection.md; not in runtime. |
| Deduplication by anomaly_id | Production-ready | Implemented in detector. |
| Suppression, cooldown, staleness | Baseline-only | since filter; no cooldown window yet. |
| Confidence or evidence summary | Baseline-only | description and recommended_response; confidence field added in schema. |

**Scope**: Active path is rule-based only. Outputs are operationally usable; no fake anomalies from synthetic data.

---

## District-Level Equity Analytics

| Item | Status | Notes |
|------|--------|------|
| File-based district_scores.json | Baseline-only | Real or recorded data only; no synthetic default in main path. |
| Composite score (pt + modal + aff) / 3 | Baseline-only | Formula explicit in code; documented in fairness.md. |
| data_status when no data | Production-ready | Returns unavailable and empty districts with note. |
| Bias and limitation note | Production-ready | Note states derived analytic index; not official policy. |
| Confidence or subgroup comparison | Concept / future | Can be added when data supports it. |

**Scope**: Only file-based input; no fabricated scores. Equity response always includes data_status and note.

---

## Digital Twin Derived Scoring

| Item | Status | Notes |
|------|--------|------|
| Twin completeness / readiness | Baseline-only | data_status and source_provenance in snapshot. |
| Per-edge state (speed, occupancy, incident) | Production-ready | From real network and providers when configured. |

---

## Federated Learning Pathway

| Item | Status | Notes |
|------|--------|------|
| Federated orchestration (e.g. Flower) | Concept / future | Documented in federated-learning.md; not active in runtime. |
| Architecture readiness | Concept / future | Codebase and docs support future FL; not a production feature. |

**Scope**: FL is research pathway only. API and product must not present federated learning as an active production feature.

---

## Source Completeness and Confidence Scoring

| Item | Status | Notes |
|------|--------|------|
| data_status on snapshot and forecast | Production-ready | live, unavailable, configuration_required, etc. |
| source_provenance on snapshot | Production-ready | Per-source status and note. |
| Confidence on forecast/anomaly/equity | Baseline-only | Fields added; semantics documented (e.g. baseline has no calibrated confidence). |

---

## Uncertainty Estimation

| Item | Status | Notes |
|------|--------|------|
| Forecast uncertainty band | Concept / future | Baseline has no calibrated uncertainty; can be added with statistical baseline. |
| Interval estimation in equity | Concept / future | Not implemented. |

---

## Data Quality Scoring

| Item | Status | Notes |
|------|--------|------|
| Source freshness, missingness | Baseline-only | Provenance includes fetched_at; no aggregate quality score yet. |
| Drift or staleness thresholds | Concept / future | To be added in quality-control layer. |

---

## Route Recommendation Logic

| Item | Status | Notes |
|------|--------|------|
| Weighted objective scoring | Baseline-only | _weight() in plan.py; time, cost, carbon. |
| Ranking of alternatives | Baseline-only | Single alternative in baseline; multi-alternative planned. |

---

## Disruption-Aware Rerouting

| Item | Status | Notes |
|------|--------|------|
| Incident flag on edges | Production-ready | Twin edges carry incident; routing uses current twin. |
| Explicit reroute API | Concept / future | "Reroute" is recompute with same API and updated twin. |

---

## Summary: Active vs Inactive

- **Active in main path**: Heuristic forecast baseline, rule-based anomaly detection, file-based equity score, weighted routing baseline, digital twin state and provenance. All use real or recorded data or explicit baseline logic; no synthetic runtime substitution.
- **Explicitly baseline or future**: ST-GNN, statistical anomaly (z-score), federated learning, ETA prediction, forecast uncertainty bands, data quality scores, multi-alternative ranking. These are either documented as future or implemented as non-production experiments.
- **Removed or never added**: No fabricated model outputs; no synthetic fallbacks in active AI endpoints. Placeholder route is only when no path exists and is clearly labeled.

This audit is the source of truth for product scope and for separating production baselines from experimental or future work.

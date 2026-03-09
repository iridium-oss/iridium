# AI Architecture

This document summarizes the AI and scoring architecture of IRIDIUM: what runs in production, how data flows to models, and how outputs are governed. It aligns with [ai-capability-audit.md](ai-capability-audit.md).

## Production AI Components

| Component | Role | Data source | Output metadata |
|-----------|------|-------------|------------------|
| Forecasting | Short-horizon congestion/speed | Digital twin (assembled snapshot) | model_type, model_maturity, data_status, source_coverage, confidence_note |
| Anomaly detection | Incidents, demand surge | Digital twin (assembled snapshot) | model_type, model_maturity, source_type, evidence_summary |
| Equity score | District-level composite | File (district_scores.json) | model_type, model_maturity, data_status, source_coverage, confidence_note |
| Routing | Weighted path | Digital twin (assembled snapshot) | model_type, model_maturity, data_status, fallback_used |

All use **real or recorded data only**. No synthetic runtime substitution in the main path.

## Data to Model Pipeline

1. **Digital twin**: state_assembler builds snapshot from PostGIS (network), weather, and traffic when configured. Result is DigitalTwinSnapshot with nodes, edges, data_status, source_provenance.
2. **Forecast**: Pipeline reads snapshot, uses edges for baseline heuristic; returns CongestionForecastResponse with full metadata.
3. **Anomaly**: Detector reads snapshot edges, applies rule-based checks (incident flag, occupancy > 85%); returns list of AnomalyEvent with source_type and evidence_summary.
4. **Routing**: Plan reads snapshot, builds graph, runs weighted path search; on empty graph or no path, returns explicit fallback and fallback_used True.
5. **Equity**: Score reads from EQUITY_DATA_PATH/district_scores.json; on missing path or file, returns empty districts and data_status unavailable.

Every step is traceable: responses reference data_status, source_coverage, and model_type so that outputs can be tied to upstream data and baseline logic.

## Model Governance

- **Version**: Baselines are code-defined; model_version (e.g. baseline-heuristic) is set in response.
- **Maturity**: production_baseline for all active paths; experimental or inactive for future/optional paths.
- **Artifacts**: No external model artifacts are loaded for current production. When a learned model is added, it must reference dataset version, feature version, and training config in metadata.

## Experimental and Future

- ST-GNN forecasting: documented in [modeling.md](modeling.md); not in runtime.
- Statistical anomaly (z-score, rolling baseline): documented in [anomaly-detection.md](anomaly-detection.md); not in runtime.
- Federated learning: documented in [federated-learning.md](federated-learning.md) and [federated-learning-status.md](federated-learning-status.md); not active.

See [model-reliability.md](model-reliability.md) for serving and degradation behavior and [ai-capability-audit.md](ai-capability-audit.md) for the full classification.

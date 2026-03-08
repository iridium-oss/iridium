# Evaluation Plan

This document defines how IRIDIUM components are evaluated: metrics, baselines, data splits, and reporting. It supports reproducibility and fair comparison. The repository currently implements baseline components (heuristic forecast, baseline routing, synthetic equity scores, rule-based anomalies); evaluation will apply to these and to future ST-GNN and federated components.

## Forecasting

- **Targets**: Congestion level, speed, or occupancy at segment or network level. Horizon: 2 to 3 hours; resolution (e.g. 15 min) to be fixed in implementation.
- **Metrics**: MAE $\frac{1}{n}\sum_i |y_i - \hat{y}_i|$, RMSE $\sqrt{\frac{1}{n}\sum_i (y_i - \hat{y}_i)^2}$, MAPE where appropriate. For categorical targets (e.g. congestion level): accuracy or F1. Metrics will be reported overall and, where meaningful, by time-of-day and by region.
- **Baselines**: Persistence (last observed value), historical average, simple propagation. Same preprocessing and split for all methods.
- **Splits**: Temporal; e.g. last 20% of time for test, preceding for validation, rest for train. No future leakage.
- **Federated setting**: When evaluating the global model, test data may be held out per participant or centralised (non-personal) depending on what is being measured. Protocol will be documented.

## Routing

- **Metrics**: Route quality (total time, cost, carbon) compared to a reference (e.g. shortest path, or external router). User acceptance or A/B metrics if pilot data is available.
- **Validation**: Correctness on known OD pairs; consistency with digital twin state; behaviour under incidents (reroute reflects closure).
- **Baselines**: Static routing (no real-time twin); or comparison to existing routing tools where comparable.

## Mobility Equity Score

- **Metrics**: Indicator values per district; comparison across districts and over time. No single "accuracy" metric; instead, transparency of definition and sensitivity analysis.
- **Validation**: Reproducibility of scores from same data and config; sensitivity to indicator choice and to data coverage (e.g. missing districts). Documentation of bias risks as in [docs/fairness.md](../docs/fairness.md) and [risks-and-limitations.md](risks-and-limitations.md).

## Anomaly Detection

- **Metrics**: Precision, recall, F1 (and latency from event to detection) when labelled incident data is available. When not available, qualitative review and operational feedback.
- **Validation**: Controlled tests with injected anomalies; comparison to external incident feeds where possible.

## Reporting

- Results will be reported in evaluation reports or release notes with: dataset description (or synthetic data description), split strategy, metrics, baselines, and version/commit of code and config.
- No claim of production or pilot results unless officially conducted and announced. Negative results (e.g. model underperforming baseline) will be reported honestly.

## Revisions

This plan will be updated as new components or metrics are added. Changes will be documented in this file and referenced in the CHANGELOG when relevant.

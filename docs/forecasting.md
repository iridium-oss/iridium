# Forecasting Engine

This document describes the IRIDIUM forecasting module: problem definition, production baseline, interfaces, and experimental path. It matches the implemented system.

## Problem Definition

Short-horizon (2 to 3 hour) congestion or traffic state forecast per segment. Outputs include predicted speed, congestion score, and occupancy at discrete time steps over the horizon. Target geography or graph nodes are specified via optional segment IDs.

## Production Baseline

The current production path uses a **deterministic heuristic baseline** only. No learned model is loaded or invoked.

- **Input**: Digital twin snapshot (assembled from real sources). Edges provide current speed_kmh and occupancy_pct when available.
- **Logic**: Time decay applied to base occupancy; speed derived from congestion. No trained parameters.
- **Output**: List of ForecastSegment with segment_id, timestamp, speed_kmh, congestion_score, occupancy_pct.

Every response includes:

- `model_version`: baseline-heuristic
- `model_type`: deterministic_baseline
- `model_maturity`: production_baseline
- `data_status`: From twin (live, unavailable, configuration_required)
- `source_coverage`: Summary of upstream data (e.g. twin_edges count)
- `confidence_note`: States that baseline has no calibrated uncertainty; for operational awareness only.
- `fallback_used`: False for baseline (no fallback path).

## Interfaces

- **Prediction horizon**: 1 to 180 minutes (query parameter).
- **Target segments**: Optional comma-separated segment IDs; omit for default segment.
- **Feature coverage**: Reported in source_coverage (e.g. twin_edges=N).
- **Uncertainty**: Not provided by baseline; confidence_note explains this.
- **Model version and freshness**: generated_at and model_version in every response.

## Advanced Experimental Path (ST-GNN)

ST-GNN or other learned forecasting is documented in [modeling.md](modeling.md). It is **not** in the current runtime. If present in code, it is experimental only and must not be served as production. Production endpoint returns only the heuristic baseline.

## Fallback and Degradation

If the twin has no edges, the baseline still produces segments using default constants (e.g. base_speed 30, base_occupancy 0.2). This is explicit baseline behavior, not synthetic fake data: the response carries model_type and confidence_note so consumers can interpret it. No silent substitution of fake forecasts occurs.

## Evaluation

Baseline is not trained; no accuracy metrics are claimed. Evaluation of a future learned model will use MAE, RMSE, or MAPE on held-out data and will be documented in the evaluation plan. See [model-reliability.md](model-reliability.md).

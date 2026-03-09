# Forecasting Model System Audit

Classification of every forecasting-related module as of the audit date. Ensures no fake or weak code remains in the active runtime path.

## Current Modules

| Module | Classification | Notes |
|--------|----------------|-------|
| forecasting/pipeline.py | Production-usable (baseline) | Heuristic congestion forecast from twin; deterministic_baseline; no learned model. Correct and honest. |
| forecasting/federated/* | Experimental | FL simulation with linear model; not used for main forecast API. |
| ST-GNN / Graph WaveNet | Not present | To be added as primary production model path. |
| DCRNN | Not present | To be added as benchmark baseline. |
| Simple baselines (persistence, rolling mean) | Not present | To be added as first-class baselines. |

## Active Runtime Path

- **Production**: GET /api/v1/forecast/congestion calls get_congestion_forecast() which uses _baseline_congestion() only. No learned model is loaded.
- **No fake path**: The heuristic uses real twin edges when available; when edges are empty it uses default constants with explicit model_type and confidence_note. No silent substitution of fake predictions.

## After Implementation

- **Primary path**: When a trained Graph WaveNet (or ML baseline) artifact is registered and valid, inference layer may return learned predictions with full metadata.
- **Fallback**: When no valid artifact or insufficient data, return deterministic_baseline (current heuristic) or explicit unavailable/degraded status. No fake learned output.
- **Removed**: No placeholder or misleading "ST-GNN" or "model" code in the current codebase that implies a trained model where none exists.

# Forecasting Evaluation

## Metrics

- **MAE**: Mean absolute error.
- **RMSE**: Root mean squared error.
- **MAPE**: Mean absolute percentage error (used only where denominators are safe; otherwise reported as N/A).

Computed in `forecasting/evaluation/metrics.py`. Per-horizon and aggregate summaries are supported.

## Comparison

All active models are evaluated on the **same dataset versions**. Comparison tables include Graph WaveNet, DCRNN, persistence, rolling mean, and (where applicable) linear temporal baseline. Results are stored as evaluation artifacts and machine-readable reports. No invented benchmark outcomes.

## Residual Analysis

The evaluation stack supports residual analysis; see `forecasting/evaluation/` for hooks. Coverage-aware summaries account for missingness in the mask.

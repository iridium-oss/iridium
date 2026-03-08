# Forecasting Service

Baseline congestion forecasting for IRIDIUM. Produces short-horizon (2 to 3 hour) predictions using the digital twin state and a simple heuristic. No trained graph neural network yet; the pipeline is structured so an ST-GNN can replace the baseline.

## Implemented

- get_congestion_forecast(horizon_minutes, segment_ids) returning CongestionForecastResponse.
- Baseline: heuristic congestion score and speed from current twin state with temporal decay.
- Feature assembly and graph consumption from digital twin; extension point for model inference.

## Future

- ST-GNN (e.g. PyTorch Geometric) for spatio-temporal prediction.
- Trained model loading and versioning.
- Formal evaluation against persistence and historical baselines (see research/evaluation-plan.md).

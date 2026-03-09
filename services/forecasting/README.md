# Forecasting Service

Production-grade forecasting engine for IRIDIUM. Graph WaveNet is the primary model; DCRNN and simple baselines support benchmarking and fallback. The deterministic heuristic from the digital twin remains the operational fallback when no trained artifact or insufficient history is available.

## Structure

- **task**: Forecasting task definition (target, horizon, granularity, degraded-mode policy).
- **data**: Dataset builder from digital twin snapshots; manifests record coverage and freshness.
- **graph**: Adjacency and support matrix construction from network topology.
- **features**: Versioned, deterministic feature pipeline (lags, rolling stats, time encoding).
- **baselines**: Persistence, rolling mean, linear temporal (first-class evaluation).
- **models**: Graph WaveNet (production), DCRNN (baseline), common utilities.
- **training**: Config-driven training, checkpoints, temporal splits, early stopping.
- **evaluation**: MAE, RMSE, MAPE; per-horizon and comparison tables.
- **inference**: Production-safe wrapper; no fake forecasts when artifact is missing.
- **registry**: Model metadata and validation before load.
- **configs**: YAML config for Graph WaveNet (and training).
- **artifacts**: Checkpoints and metadata (gitignored).
- **tests**: Task, graph, data, baselines, models, inference, registry.

## Implemented

- Congestion forecast API (GET /forecast/congestion) with deterministic baseline and clear model_type/fallback_used.
- GET /forecast/status, /forecast/models, /forecast/coverage, /forecast/features.
- Graph WaveNet and DCRNN implementations; simple baselines; dataset builder; graph construction; training runner; evaluation metrics; inference wrapper; model registry.
- Documentation: docs/forecasting-architecture.md, forecasting-models.md, forecasting-data-pipeline.md, forecasting-evaluation.md, forecasting-serving.md, forecasting-limitations.md.

## Usage

- **Training**: Run `forecasting.training.run_training` with data array, support matrix, entity order, and config; artifact_dir to save checkpoints.
- **Inference**: Use `ForecastInferenceWrapper` with FORECAST_ARTIFACT_DIR (or pass artifact_dir); load(entity_order) then predict(x, support, entity_ids).
- **API**: Set FORECAST_ARTIFACT_DIR for /forecast/status and /forecast/models to reflect loaded artifact.

## Dependencies

iridium-schemas, pydantic, numpy, torch, scipy. Optional: digital-twin and network/DB for full pipeline.

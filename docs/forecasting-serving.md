# Forecasting Serving

## Inference Layer

`forecasting/inference/wrapper.py`: Production-safe wrapper that:

- Loads a registered artifact only after validation (entity order, maturity).
- Returns **InferenceResult** with: prediction array, horizon_steps, entity_ids, model_name, model_version, dataset_version, feature_version, coverage_note, reliability_note, degraded flag, optional latency_ms.
- Never returns learned forecasts when the artifact is missing or invalid; the caller should use deterministic or statistical baseline or respond with unavailable.

Inference is bounded in latency (configurable max); caching may be added where safe (e.g. same input fingerprint).

## API

- **GET /api/v1/forecast/status**: Engine status (model loaded, degraded).
- **GET /api/v1/forecast/models**: Registered model metadata (family, version, maturity).
- **GET /api/v1/forecast/coverage**: Task spec coverage (horizon, input window, min_coverage_ratio, granularity).
- **GET /api/v1/forecast/features**: Feature schema version and names.
- **GET /api/v1/forecast/congestion**: Congestion forecast. Response fields **model_type** and **model_maturity** distinguish: learned model output, statistical baseline, deterministic fallback, unavailable. **fallback_used** is true when a fallback path was used.

## Health and Observability

Production readiness includes: structured logs, model loading checks, stale-artifact detection, insufficient-coverage checks, explicit degraded mode, and health/observability surfaces for inference latency, model version, coverage status, and recent inference counts.

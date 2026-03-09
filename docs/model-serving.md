# Model Serving

This document describes how AI and scoring models are served via the API: contracts, metadata, and safe behavior. See [model-reliability.md](model-reliability.md) for reliability and confidence semantics.

## API Contracts

- **Forecast**: GET /api/v1/forecast/congestion. Returns CongestionForecastResponse (segments, horizon_minutes, generated_at, model_version, model_type, model_maturity, source_coverage, confidence_note, fallback_used, note, data_status). Pydantic models; stable field names; explicit units (e.g. speed_kmh, occupancy_pct).
- **Anomaly**: GET /api/v1/anomalies. Returns JSON with anomalies list plus model_type, model_maturity, data_status, note. Each anomaly has anomaly_id, type, severity, segment_ids, detected_at, optional confidence, source_type, evidence_summary.
- **Equity**: GET /api/v1/equity/score. Returns MobilityEquityScore (districts, generated_at, note, data_status, model_type, model_maturity, source_coverage, confidence_note).
- **Routing**: POST /api/v1/routing/plan. Returns RouteResponse (alternatives, requested_at, note, model_type, model_maturity, data_status, fallback_used).

All AI-related outputs are structured and include provenance or model metadata so that frontend, operators, and researchers can interpret them.

## Request Validation

- Forecast: horizon_minutes 1 to 180; segment_ids optional.
- Routing: origin/destination lat/lon in valid ranges; modes list; optimize one of time, cost, carbon.
- Equity: optional district_ids filter.
- Anomaly: optional segment_ids and since.

Invalid requests return validation errors; no silent coercion to fake success.

## Failure and Degradation

- If no valid model or data path can run, the endpoint returns a truthful response: empty list, data_status unavailable, or fallback with fallback_used True and a clear note. No fabricated success or fake intelligence.
- Latency: endpoints are synchronous; long-running work should be bounded (e.g. path search limited by graph size in a future revision).

## Consumers

Outputs are designed to be consumable by frontend developers, operators, and researchers: explicit units, uncertainty or confidence notes, and model maturity so that UI and analytics can display or filter appropriately.

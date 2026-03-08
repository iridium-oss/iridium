# API Specification

This document describes the IRIDIUM API as implemented. Request and response shapes are defined by Pydantic models in `packages/schemas` and exposed via FastAPI; OpenAPI is available at `/docs` when the API is running.

## Base URL and Versioning

- Base URL is deployment-specific (e.g. `http://localhost:8000` for local dev).
- API routes are under `/api/v1/`. Health and version are at `/health` and `/version`.
- All responses are JSON. Error responses use HTTP status codes and a detail payload.

## Authentication

Public endpoints are unauthenticated in the baseline. Administrative or write endpoints (e.g. ingestion) may require authentication in future; mechanism will be documented when added.

## Endpoints summary

| Endpoint | Method | Purpose | Data source | Response status |
|----------|--------|---------|--------------|------------------|
| /health | GET | Liveness | None | 200 ok |
| /version | GET | Version info | Config | 200 |
| /api/v1/network/graph | GET | Digital twin snapshot | State assembler (OSM, weather, traffic) | 200; data_status in body |
| /api/v1/forecast/congestion | GET | Congestion forecast | Twin + heuristic/ST-GNN | 200; data_status in body |
| /api/v1/routing/plan | POST | Multimodal route | Twin, optional OTP/Valhalla | 200 |
| /api/v1/equity/score | GET | Mobility Equity Score | EQUITY_DATA_PATH or unavailable | 200; data_status in body |
| /api/v1/anomalies | GET | Active anomalies | Twin, rules, provider alerts | 200 |
| /api/v1/ingestion/events | POST | Submit batch | Validation only | 200/400 |

## Endpoints (Implemented)

### Health and version

- **GET /health**  
  Liveness check. Returns 200 and `{"status": "ok"}`.

- **GET /version**  
  Returns `{"api_version": "v1", "app_version": "<APP_VERSION>", "service": "iridium-api"}`.

### Network

- **GET /api/v1/network/graph**  
  Returns the current digital twin snapshot: `nodes`, `edges`, `snapshot_at`, `version`. Schema: DigitalTwinSnapshot (see packages/schemas/iridium_schemas/network.py).

### Forecasting

- **GET /api/v1/forecast/congestion**  
  Short-horizon congestion forecast.  
  Query: `horizon_minutes` (default 120, 1-180), `segment_ids` (optional, comma-separated).  
  Response: `segments` (list of segment_id, timestamp, speed_kmh, congestion_score, occupancy_pct), `horizon_minutes`, `generated_at`, `model_version`, `note`. Baseline: heuristic; ST-GNN planned.

### Routing

- **POST /api/v1/routing/plan**  
  Multimodal route planning.  
  Body: RouteRequest (origin_lat, origin_lon, destination_lat, destination_lon, modes, max_transfers, optimize, departure_time).  
  Response: RouteResponse with `alternatives` (list of RouteAlternative: segments, total_duration_min, total_cost, total_carbon_kg, transfer_count, score_*), `requested_at`, `note`. Baseline optimizer.

### Equity

- **GET /api/v1/equity/score**  
  Mobility Equity Score by district.  
  Query: `district_ids` (optional, comma-separated).  
  Response: `districts` (district_id, district_name, avg_travel_time_to_services_min, pt_accessibility_proxy, modal_availability_proxy, affordability_proxy, composite_score), `generated_at`, `note`.

### Anomalies

- **GET /api/v1/anomalies**  
  Active anomalies.  
  Query: `segment_ids` (optional), `since` (optional, datetime).  
  Response: `{"anomalies": [AnomalyEvent, ...]}`. Each has anomaly_id, type, severity, segment_ids, zone_id, detected_at, valid_from, valid_to, description, recommended_response.

### Ingestion

- **POST /api/v1/ingestion/events**  
  Submit a batch of ingestion events. Body: IngestionEventBatch (sensor_events, gnss_points, weather, public_events, energy_signals). Validation only in baseline; no persistence. Raw personal data must not be included.

## Data Contracts

Schemas are in `packages/schemas` (Pydantic). The API uses them for request/response validation and OpenAPI generation. See packages/schemas/README.md and the iridium_schemas package.

## Rate Limits and Errors

Rate limits are not implemented in the baseline. 400 for validation errors (detail contains message or list of errors); 500 for server errors. No sensitive details in production error bodies.

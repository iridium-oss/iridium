# Shared Schemas

Pydantic models and data contracts shared by the API, ingestion, and services. All ingestion and API request/response shapes are defined here for consistency and validation.

## Contents

- **events**: SensorEvent, GNSSPoint, WeatherSnapshot, PublicEventRecord, EnergyGridSignal, IngestionEventBatch
- **network**: NetworkNode, NetworkEdge, DigitalTwinSnapshot
- **forecast**: CongestionForecastResponse, ForecastSegment
- **routing**: RouteRequest, RouteResponse, RouteSegment, RouteAlternative
- **anomaly**: AnomalyEvent
- **equity**: MobilityEquityScore, DistrictScore

## Usage

```python
from iridium_schemas import RouteRequest, RouteResponse, AnomalyEvent
```

Install in development: `pip install -e ./packages/schemas` from repo root.

## JSON Schema

Pydantic v2 can export JSON Schema via `model.model_json_schema()`. Use for OpenAPI or external contract validation. The API exposes these via FastAPI's automatic OpenAPI generation.

## Privacy

Schemas do not include fields that identify individuals or devices. GNSS and telemetry are assumed aggregated or anonymised at source before ingestion.

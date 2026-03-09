# Data Sources

IRIDIUM integrates multiple heterogeneous data streams. This document describes the intended sources, their purpose, expected schema direction, quality concerns, and privacy considerations. Schemas are authoritative when defined in `data-contracts/`; this doc provides context.

Note: code-level shared contracts live under `packages/schemas` in this repository. This document describes intended semantics, not an alternative schema source.

## IoT Road Sensors

**Purpose**: Real-time traffic state (speed, occupancy, flow) on road segments. Primary input for the digital twin and congestion forecasting.

**Expected schema direction**: Time-series records with segment identifier, timestamp, and metrics (e.g. speed_kmh, occupancy_pct, flow_count). Segment IDs align with the digital twin graph.

**Quality concerns**: Missing or stale readings, sensor drift, and misalignment of segment boundaries. Ingestion should validate ranges and handle gaps (e.g. interpolation or flagging).

**Privacy considerations**: Sensor data is typically non-personal. If sensors are linked to identifiable devices, that linkage must not be exposed in central systems. Prefer aggregated or anonymised feeds.

## GNSS Telemetry

**Purpose**: Movement and speed of vehicles or devices to infer traffic conditions and demand. Used with care to avoid re-identification.

**Expected schema direction**: Aggregated or anonymised trajectories or link-level counts; or encrypted/local-only raw data with only derived features (e.g. segment speeds) sent to the twin. Exact schema depends on the privacy model (e.g. local aggregation at the participant).

**Quality concerns**: GPS noise, multipath, and sampling bias. Aggregation and map-matching quality affect usefulness.

**Privacy considerations**: Raw GNSS can be highly identifying. IRIDIUM assumes that raw telemetry is processed locally or by a trusted party; only non-identifying aggregates or features enter central or shared systems. Data contracts will not define fields that directly identify individuals or devices.

## Meteorological Feeds

**Purpose**: Weather conditions (precipitation, temperature, visibility) that influence demand and road state. Used as contextual features in forecasting and optionally in routing.

**Expected schema direction**: Time-stamped records with location (or city/region), and standard weather variables. May be external API or batch files.

**Quality concerns**: Latency, resolution (temporal and spatial), and units. Normalisation and alignment to forecast horizons are required.

**Privacy considerations**: Typically no personal data. Licence and attribution for the provider must be respected.

## Public Event Calendars

**Purpose**: Events (sports, concerts, holidays) that cause demand spikes or route changes. Used for demand forecasting and anomaly context.

**Expected schema direction**: Events with start/end time, location or venue, and optional capacity or type. Integration may be pull (API) or push (feed).

**Quality concerns**: Completeness and timeliness. Missing or late events reduce forecast accuracy.

**Privacy considerations**: Public events are generally non-personal. Organiser or venue data may be subject to terms of use.

## Energy Grid Signals

**Purpose**: Optional. Future use for electric mobility (charging demand) or grid-aware operations. Not required for the initial roadmap.

**Expected schema direction**: Time-varying signals (e.g. price, capacity) at zone or substation level. To be defined when the feature is prioritised.

**Quality concerns**: Availability and granularity of open or partner data.

**Privacy considerations**: Grid data is typically non-personal. Commercial or operational sensitivity may apply to some signals.

---

For each source, the ingestion pipeline is responsible for validation, normalisation, and mapping into the digital twin and, where applicable, into training data. Data contracts will specify the exact fields and types used inside the platform.

# Data Retention

IRIDIUM retention policy for data stored or processed by the platform. Deployers must align with local law and operator agreements.

## Principles

- Retain only what is necessary for the stated purpose (forecasting, routing, equity analytics, anomaly detection).
- Personal or device-level data must have the shortest retention consistent with consent and legal requirements.
- Provenance and snapshot metadata may be retained longer than raw observations for audit and reproducibility.

## Categories

### Network Topology (OSM-derived)

- Processed network (nodes, edges) in PostGIS: retain until superseded by a new import. No automatic expiry.
- Raw OSM PBF: not stored in repository; local cache may be retained per fetch script; document retention in runbook if applicable.

### Transit (GTFS)

- Static GTFS: retain current and previous version when feed is updated; older versions may be purged after a defined period (e.g. 90 days) unless operator terms require otherwise.
- Realtime trip/vehicle data: do not persist longer than required for real-time routing (e.g. in-memory or short TTL cache). No long-term storage of vehicle positions unless explicitly permitted.

### Traffic and Speed Observations

- Segment speeds and travel times: retain according to provider terms and operational need. Typical: rolling window (e.g. 7-30 days) for historical features; do not retain indefinitely without a defined purpose.

### Telemetry (GNSS)

- Consent-based device positions: retain only as long as consent and privacy policy specify. Pseudonymous IDs; no raw identity. Minimum retention; purge when no longer needed for consented purpose. See docs/telemetry-consent.md.

### Weather

- Historical and forecast: retain for feature store and model training as needed; document retention in pipeline config. Open-Meteo data may be cached per API terms.

### Events

- Event listings: short retention (e.g. event end date plus a short buffer). Do not build permanent profiles from event data.

### Anomalies and Forecasts

- Anomaly records: retain for operational review and audit (e.g. 90 days).
- Forecast snapshots: retain for evaluation and debugging per research/evaluation-plan.md; purge when no longer needed.

### Digital Twin Snapshots

- Materialized snapshots: retain according to operational need; document in deployment runbook. Include provenance so that snapshot can be reproduced or deprecated.

## Configuration

Retention intervals are configured via environment or config file (e.g. RETENTION_OBSERVATIONS_DAYS). Defaults must be conservative. No retention of personal data beyond the minimum required and consented.

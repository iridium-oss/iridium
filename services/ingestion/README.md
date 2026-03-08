# Ingestion Service

Baseline ingestion pipeline for IRIDIUM. It reads sample or synthetic data from the filesystem, validates records against shared schemas, and stages them for consumption by the digital twin. Raw personal data is not accepted; GNSS and telemetry are assumed aggregated or anonymised at source.

## Implemented

- Validation of IngestionEventBatch (sensor, GNSS, weather, public events).
- File-based loading from data/samples and data/synthetic (JSON/CSV).
- run_ingestion(samples_dir, synthetic_dir) returns record count and validation errors.
- No central persistence of raw records; the digital twin service consumes staged or streamed state.

## Future Evolution

- Streaming ingestion (Kafka, Redis, or HTTP push) with backpressure and idempotency.
- Direct write to digital twin store or message queue for real-time updates.
- Schema versioning and compatibility checks.

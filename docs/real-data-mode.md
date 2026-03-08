# Real-Data Mode

IRIDIUM is configured for real data and real integrations. Synthetic data is not used in the primary demo or runtime path. When a source is unavailable or not configured, the application returns an explicit status (unavailable, configuration_required, permission_required) and does not substitute invented data.

## What Runs on Real Data

- **Network**: Loaded from OSM (Geofabrik Azerbaijan) via fetch script and network-import into PostGIS. When not loaded, network graph is empty and data_status is configuration_required.
- **Weather**: Open-Meteo API for Baku and Quba. Live when API is reachable; unavailable on failure.
- **Transit**: Provider registry only. Baku Metro and BakuBus are permission_required until operator provides GTFS. No fabricated GTFS.
- **Traffic**: Provider adapter when TRAFFIC_API_KEY (or equivalent) is set. Otherwise configuration_required; no synthetic traffic.
- **Telemetry**: Traccar when configured and consent in place. Otherwise unavailable.
- **Events**: Real event ingestion when source is configured and ToS compliant. Otherwise unavailable.
- **Energy context**: Real sources when licensed and configured. Otherwise unavailable.
- **Digital twin**: State assembler merges only real sources; snapshot includes data_status and source_provenance.
- **Forecast**: Uses twin state; data_status propagated. Heuristic baseline when no trained model; no fabricated metrics.
- **Equity**: Real administrative boundaries and accessibility from OSM/transit when available. No hardcoded synthetic district scores in main path.
- **Anomaly**: Real inputs (traffic deviations, provider alerts, event surges) when available. No synthetic anomaly streams in main path.

## Configuration Modes

- **Public-only**: OSM fetch + network-import, Open-Meteo weather. No traffic or transit feeds. UI shows configuration_required for those.
- **Premium-traffic**: Add TRAFFIC_API_KEY and provider adapter. Traffic layer can be live.
- **Operator-integration**: Add GTFS feed URL and terms for Baku Metro/BakuBus when provided. Transit and routing can use real schedules.

See docs/provider-matrix.md and docs/operator-integration-requirements.md.

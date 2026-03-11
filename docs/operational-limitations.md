# Operational Limitations

Honest statement of what is and is not implemented or guaranteed in the current IRIDIUM platform.

## Implemented

- Data governance and provenance documentation (data-provenance, source-licensing, data-retention, privacy-notes, operator-integration-requirements).
- OSM fetch script for Azerbaijan (Geofabrik); manifest with timestamp and checksum.
- Weather ingestion from Open-Meteo (real); no synthetic weather in main path.
- Transit provider registry (Baku Metro, BakuBus) with status permission_required; no fabricated GTFS.
- Traffic provider abstraction; configuration_required when credentials absent; no synthetic traffic.
- Digital twin state assembler; real sources only; data_status and source_provenance in snapshot.
- API network and forecast endpoints return data_status; no silent synthetic substitution.
- Schemas for provenance and provider registry.

## Not Implemented (Gaps)

- **Network import into PostGIS**: Fetch script and network-import service (load_network_from_db) exist. Graph remains empty until OSM is fetched, imported into PostGIS, and DB is enabled; then digital twin uses it.
- **GTFS load**: When operator provides feed, GTFS load and validation pipeline to be added. No invented feed.
- **Traffic provider adapter**: Interface exists; TomTom (or other) adapter implementation is not done. When key is set, status remains configuration_required until adapter is implemented.
- **Traccar integration**: Documented; integration code not in place. Telemetry layer unavailable until implemented.
- **Event ingestion**: Documented; adapters for iTicket/CityLife not implemented. Event layer unavailable or permission_required.
- **Energy context pipeline**: Documented; no implementation. Unavailable until added.
- **OpenTripPlanner and Valhalla**: Not integrated. Routing still uses baseline path when graph is empty; no OTP/Valhalla in main path yet.
- **Federated learning (Flower)**: Simulation and institution-lab use only; API returns honest status (active False, runs/models empty). See services/forecasting/federated.
- **Learned forecast model**: Graph WaveNet and DCRNN code and inference wrapper exist; training and artifact production are separate. API uses deterministic baseline when no artifact or historical inputs; model_loaded in forecast/status reflects FORECAST_ARTIFACT_DIR.
- **Recorded real snapshots**: Mechanism for storing and serving recorded snapshots with provenance is not fully in place; when implemented, must follow docs/data-provenance.md.

## Dependencies on External Agreements

- Baku Metro and BakuBus GTFS: operator or authorised body must provide feed.
- TomTom or other traffic provider: contract and API key.
- Event sources: ToS and rate limits must be respected; some sources may require partnership.

## No Claims

- No claim of production readiness where only integration scaffolding exists.
- No claim of regulatory or legal compliance as a guaranteed fact.
- No fabricated feeds, benchmarks, or metrics. Only show metrics when computed from real collected data.

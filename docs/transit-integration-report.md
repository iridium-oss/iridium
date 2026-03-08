# Baku Transit Integration - Final Output Report

## Providers added

- **bakubus_ayna**: BakuBus via AYNA public map API. Fetches route list from `GET https://map-api.ayna.gov.az/api/bus/getBusList` and route details from `GET https://map-api.ayna.gov.az/api/bus/getBusById?id={bus_id}`. source_family=public_api, source_status=public_undocumented. Live when AYNA is reachable.
- **bakumetro_official**: Baku Metro from official website. Static network: Red, Green, Purple lines; station names; interchange pairs; service window; fare policy. source_family=official_website, source_status=static_schedule_only. No machine-readable GTFS from operator.

Registry entries for operator GTFS (baku_metro, bakubus) remain permission_required.

## Endpoints used

- AYNA: `https://map-api.ayna.gov.az/api/bus/getBusList`, `https://map-api.ayna.gov.az/api/bus/getBusById?id={id}`.
- Baku Metro: No HTTP endpoint; static data from documented official site structure (line names, station lists, interchanges, operating hours, fare).

## Data fields integrated

- **BakuBus (AYNA)**: carrier, number, firstPoint, lastPoint, tariff, durationMinuts, stops (id, name, lat, lon), flowCoordinates. Normalized to TransitAgency, TransitRoute, TransitRouteVariant, TransitStop, TransitStopSequenceEntry, TransitShapePoint, TransitFarePolicy. Provenance: source URL, fetched_at, response checksum; raw cache in .transit_cache (gitignored).
- **Baku Metro**: Agency, routes (red, green, purple), stops (station names; coordinates left for OSM resolution), interchanges, TransitServiceWindow, TransitFarePolicy. No coordinates in static model; no timetable.

## What could be exported to GTFS

- agency.txt (Baku Metro, BakuBus).
- routes.txt (metro lines and bus routes when fetched).
- stops.txt (stops with coordinates when present; metro stops without coordinates until OSM resolution).
- shapes.txt (from AYNA flowCoordinates when bus routes are fetched).
- README.txt with repository-generated label.

## What could not yet be exported honestly

- trips.txt and stop_times.txt: exact timetable not available from AYNA or metro static; omitted to avoid fabricated schedule.
- calendar.txt / calendar_dates.txt: not justified by current sources.
- Metro stop coordinates: not in static source; require OSM resolution and validation (ambiguous matches flagged for manual review).

## What remains needed for full routing-quality deployment

- Exact stop_times or defensible timetable for metro and/or bus when such data is officially or publicly available.
- OSM-based coordinate resolution for metro stations with validation and manual review of ambiguous matches.
- GTFS Realtime (trip updates, vehicle positions) when provided by operator or authorised source.
- Operator-issued GTFS for Baku Metro and BakuBus when and if provided under terms.

## API endpoints

- GET /api/v1/transit/providers
- GET /api/v1/transit/routes?bakubus_limit=0|N
- GET /api/v1/transit/stops?bakubus_limit=0|N
- GET /api/v1/transit/network?bakubus_limit=0|N
- GET /api/v1/transit/readiness
- GET /api/v1/transit/gtfs/status

## Frontend

- Dashboard Transit page: providers with status badges, routes table, readiness (static stop discovery, route visualization, transfer graph, timetable routing), GTFS status. No fake realtime arrival predictions.

## Documentation

- docs/baku-transit-integration.md
- docs/transit-data-governance.md
- docs/gtfs-generation.md
- docs/provider-matrix.md (updated with BakuBus AYNA and Baku Metro official)
- services/transit-ingestion/README.md

## Tests

- tests/test_transit_baku.py: BakuBus list and route normalization, metro static network, readiness report, canonical schema validation, GTFS builder (core files, no stop_times/trips), provider registry and status, OSM resolution (empty name, mock no-candidates, mock single-candidate high confidence), flag_ambiguous_for_manual_review.

## Implementation details (this pass)

- AYNA client: retry with backoff (MAX_RETRIES, RETRY_BACKOFF) for getBusList and getBusById.
- Metro OSM: osm_resolution.py for Nominatim-based station coordinates; OsmValidationReport and flag_ambiguous_for_manual_review for validation.
- Storage: get_feed_export_dir() (IRIDIUM_GTFS_OUTPUT_DIR or feed_export); GTFS builder uses it when output_dir is None.

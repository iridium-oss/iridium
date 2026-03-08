# Transit Ingestion

Real public-transport integration for BakuBus and Baku Metro. Unified transit model, normalization, GTFS builder, and routing preparation. No fabricated feeds or timetables.

## Architecture

- **providers/bakubus_ayna**: AYNA map API client (getBusList, getBusById). Normalization to canonical schema. Provenance and raw cache.
- **providers/bakumetro_official**: Static Baku Metro network from official website (lines, stations, interchanges, service window, fare). Coordinates via OSM resolution and validation.
- **normalization**: Merge both providers into one snapshot (agencies, routes, stops, shapes, interchanges, fare, service).
- **gtfs_builder**: Build GTFS Static from snapshot. Repository-generated label; no operator-issued claim. Only defensible files (agency, routes, stops, shapes; no fabricated stop_times).
- **validation**: Readiness report (static stop discovery, route visualization, transfer graph, timetable routing). Honest about missing stop_times.
- **storage**: Raw response cache (gitignored .transit_cache).

## Provider status

- **bakubus_ayna**: source_family=public_api, source_status=public_undocumented. Live when AYNA is reachable.
- **bakumetro_official**: source_family=official_website, source_status=static_schedule_only. No machine-readable GTFS from operator.

## Usage

- API: `GET /api/v1/transit/providers`, `/transit/routes`, `/transit/stops`, `/transit/network`, `/transit/readiness`, `/transit/gtfs/status`.
- Build GTFS: call `transit_ingestion.gtfs_builder.build.build_gtfs_static(snapshot, output_dir)`.
- See docs/baku-transit-integration.md, docs/transit-data-governance.md, docs/gtfs-generation.md.

## Dependencies

- iridium-schemas (canonical transit types)
- httpx (AYNA client)

# Baku Transit Integration

This document describes how BakuBus and Baku Metro are integrated into the IRIDIUM transit layer using only real, publicly accessible or officially published information. No GTFS feeds, stop coordinates, or timetables are invented.

For **March 2026 statistics baseline** (fares, network figures, ridership, source links), see [baku-transit-statistics-baseline.md](baku-transit-statistics-baseline.md).

## Overview

- **BakuBus**: Integrated via the public AYNA map API. Route list from `getBusList`; route details (stops, geometry, fare, duration) from `getBusById`. Treated as source_family=public_api, source_status=public_undocumented.
- **Baku Metro**: Integrated from the official metro website. Line names, station names, interchange relationships, line-level length and station count, operating hours and fare information. Treated as source_family=official_website, source_status=static_schedule_only. No machine-readable GTFS is assumed from the operator.

## BakuBus (AYNA)

### Endpoints used

- `GET https://map-api.ayna.gov.az/api/bus/getBusList` - Public. Returns list of bus/route identifiers.
- `GET https://map-api.ayna.gov.az/api/bus/getBusById?id={bus_id}` - Public but undocumented. Returns carrier, number, firstPoint, lastPoint, tariff, durationMinuts, stops, flowCoordinates.

### Data normalized

- Operator (BakuBus), route (short_name from number), route variant (first_point, last_point), stops (id, name, lat, lon where present), stop_sequence, shape (flowCoordinates), basic fare (tariff). Provenance (source URL, fetched_at, response checksum) recorded on every fetch. Raw responses cached under `.transit_cache/bakubus_ayna/` (gitignored).

### Client behaviour

- Retries: up to MAX_RETRIES + 1 attempts with RETRY_BACKOFF between attempts for getBusList and getBusById. Timeout and rate limiting (MIN_REQUEST_INTERVAL) applied.

### What is not fabricated

- No invented route IDs, stop coordinates, or timetable. If a field is missing in the API response, it is left null or omitted in the canonical model.

## Baku Metro (official website)

### Source

- Official metro website as primary source of truth: line names, station names, interchange relationships, line-level lengths and station counts, operating hours, fare information.
- Static metro network built from documented Red, Green, Purple line station lists and interchange pairs. No per-trip timetable data is assumed; if exact schedules are not exposed, they are not invented.

### Station coordinates

- Resolved via OpenStreetMap (Nominatim) in `providers/bakumetro_official/osm_resolution.py`. Controlled station-name query: "{station_name}, Baku Metro, Baku, Azerbaijan". Rate limit 1 req/s for public Nominatim. Confidence: high (single candidate), ambiguous (multiple candidates; first used, flagged for review), none (no result). Validation: `flag_ambiguous_for_manual_review(report)` returns stop_ids that need manual review. Metro static network in code does not include coordinates until OSM resolution is run (optional).

### Data produced

- Agency (Baku Metro), routes (red, green, purple), stops (stations without coordinates until OSM), interchanges, service window, fare policy. timetable_available=false.

## Canonical schema

Shared schema in `packages/schemas/iridium_schemas/transit.py`: TransitAgency, TransitRoute, TransitRouteVariant, TransitStop, TransitStopSequenceEntry, TransitShapePoint, TransitInterchange, TransitFarePolicy, TransitServiceWindow, TransitSnapshotMetadata. Every record includes source_provider, source_family, source_status, fetched_at; effective_date and validation_note where appropriate.

## GTFS builder

The GTFS builder converts normalized BakuBus and Baku Metro data into a repository-generated GTFS Static package. It is clearly labeled as repository-generated from official and public sources; not operator-issued. Generated files: agency.txt, routes.txt, stops.txt, shapes.txt (where data exists). trips.txt and stop_times.txt are omitted when exact timetable data is not available. See docs/gtfs-generation.md.

## API

- `GET /api/v1/transit/providers` - Provider registry (bakubus_ayna, bakumetro_official, plus baku_metro/bakubus permission_required).
- `GET /api/v1/transit/routes` - Unified routes; optional `bakubus_limit` to fetch up to N bus routes from AYNA.
- `GET /api/v1/transit/stops` - Unified stops.
- `GET /api/v1/transit/network` - Network summary (counts, metadata).
- `GET /api/v1/transit/readiness` - Readiness for static stop discovery, route visualization, transfer graph, timetable routing.
- `GET /api/v1/transit/gtfs/status` - GTFS build status and label.

## What remains for full OTP-grade routing

- Exact stop_times/trips when defensible timetable data is available.
- GTFS Realtime (trip updates, vehicle positions) when provided by operator or authorised source.
- Station coordinates for metro from OSM resolution with validation; ambiguous matches reviewed.
- Operator-issued GTFS for Baku Metro and BakuBus when and if provided under terms.

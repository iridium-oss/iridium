# Provider Matrix

Status of each data provider and what is required to enable it.

## Summary table

| Provider | Domain | Status | Required to enable |
|----------|--------|--------|--------------------|
| Geofabrik OSM | Network | Public | Run scripts/fetch_osm_azerbaijan.py; then network-import into PostGIS |
| Open-Meteo | Weather | Live (no key) | None; optional rate limit |
| Baku Metro (official site) | Transit | Live (static) | None; static network from official website |
| BakuBus (AYNA API) | Transit | Live (public API) | None; getBusList public; getBusById public undocumented |
| Baku Metro GTFS | Transit | permission_required | Operator feed URL and terms |
| BakuBus GTFS | Transit | permission_required | Operator feed URL and terms |
| TomTom (or other) | Traffic | configuration_required | TRAFFIC_API_KEY and adapter implementation |
| Traccar | Telemetry | Optional | TRACCAR_HOST and credentials; consent and privacy policy |
| Event sources | Events | Depends | ToS-compliant access; see docs/event-sources.md |
| Energy context | Energy | Depends | Licensed data; see docs/energy-context.md |
| OpenTripPlanner | Routing | Optional | OTP graph built from OSM + GTFS when available |
| Valhalla | Routing | Optional | VALHALLA_URL when deployed |

## Detailed provider matrix

| Source | Provider | Acquisition method | Cadence | Access type | Licensing notes | Status |
|--------|----------|--------------------|---------|-------------|-----------------|--------|
| Network | Geofabrik OSM | Download PBF; network-import to PostGIS | On demand / daily | public | ODbL; attribution | Public when run |
| Weather | Open-Meteo | HTTP API | Hourly | public | Attribution | Live |
| Transit | Baku Metro (official) | Official website; static network | On demand | official_website | Public | static_schedule_only; no machine-readable GTFS from operator |
| Transit | BakuBus (AYNA) | AYNA map API getBusList, getBusById | On demand | public_api / public_undocumented | Public | getBusById is public undocumented |
| Transit | Baku Metro GTFS | GTFS URL when provided | When published | permission_required | Operator terms | permission_required until feed |
| Transit | BakuBus GTFS | GTFS URL when provided | When published | permission_required | Operator terms | permission_required until feed |
| Traffic | TomTom or other | Licensed API | 5-15 min | configuration_required | Commercial | configuration_required without key |
| Telemetry | Traccar | Device ingestion | Near real time | optional | Consent; privacy | Unavailable until configured |
| Events | iTicket, CityLife | API or compliant scrape | 6-12 h | Depends | ToS | See docs/event-sources.md |
| Energy | National/open data | As per docs/energy-context | Low frequency | Depends | License-dependent | See docs/energy-context.md |
| Routing | OpenTripPlanner | Build graph from OSM+GTFS | On build | optional | OSM/GTFS terms | Optional |
| Routing | Valhalla | Deploy service | N/A | optional | OSM terms | Optional |

## Response Labels

API and UI use these labels for each source or panel:

- **live**: Real-time or near-real-time from provider.
- **recorded_real_snapshot**: Stored real snapshot with timestamp and provenance.
- **unavailable**: Source failed or not reachable.
- **configuration_required**: Credentials or config missing.
- **permission_required**: Operator or licence agreement needed.
- **stale**: Data older than acceptable threshold.

No synthetic or fabricated data is presented as live or recorded_real_snapshot.

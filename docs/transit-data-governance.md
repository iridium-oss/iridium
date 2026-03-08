# Transit Data Governance

Governance and truthfulness layer for Baku transit integration. Provider name, access type, status, refresh cadence, gaps, and risks are documented in code and here.

## Provider status enums

- **official_machine_readable**: Operator-published machine-readable feed (e.g. GTFS) with terms.
- **official_website**: Official website as source; parsed or static. No claim of machine-readable feed.
- **public_api**: Public API with documented contract.
- **public_undocumented**: Public but undocumented endpoint (e.g. AYNA getBusById).
- **static_schedule_only**: Schedule/network structure only; no real-time or exact timetable.
- **permission_required**: Operator or licence agreement needed.
- **unavailable**: Not available or not implemented.

## BakuBus (AYNA)

| Field | Value |
|-------|--------|
| Provider name | bakubus_ayna |
| Legal / operational access | Public. AYNA operates public bus route map service. |
| Official vs public-undocumented | getBusList is public; getBusById is public undocumented. |
| Refresh cadence | On demand (API call). |
| Allowable cache policy | Raw responses may be cached in .transit_cache (gitignored). |
| Known gaps | No GTFS Realtime; no official operator GTFS. getBusById may change without notice. |
| Known risks | Undocumented endpoint could be deprecated or rate-limited. |
| Timetable confidence | Route and stop structure only; no per-trip timetable from this source. |
| Realtime availability | None. |

## Baku Metro (official)

| Field | Value |
|-------|--------|
| Provider name | bakumetro_official |
| Legal / operational access | Official website public information. |
| Official vs public-undocumented | Official website; static extraction. |
| Refresh cadence | On demand or manual update when site structure changes. |
| Allowable cache policy | Static network in code; no raw scrape cache required. |
| Known gaps | No machine-readable GTFS from operator. Station coordinates from OSM resolution; ambiguous matches flagged. No exact per-trip timetable in integration. |
| Incomplete geometry | Metro stops have no coordinates until OSM resolution (and validation) is run. |
| Timetable confidence | Static schedule only; timetable routing not supported. |
| Realtime availability | None. |

## Missing fields (honest inventory)

- BakuBus: Realtime vehicle positions; official GTFS; exact departure times per stop.
- Baku Metro: Operator GTFS; exact departure times; realtime trip updates; coordinates until OSM resolution.

## Data quality

- All provenance (source_provider, source_family, source_status, fetched_at) attached to normalized entities.
- No synthetic substitution: if a source is unavailable or a field is missing, the system exposes status or null rather than fabricating values.

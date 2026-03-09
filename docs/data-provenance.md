# Data Provenance

Every external data source used by IRIDIUM must document provenance. This document defines the required metadata and where it is stored.

## Provenance Manifest Fields

Each connector documents:

| Field | Description |
|-------|-------------|
| source_name | Human-readable name of the source |
| acquisition_method | Download API, scrape, manual export, etc. |
| access_type | public_api, permission_required, licensed, unavailable |
| license_or_terms | URL or short description of terms |
| refresh_cadence | How often data is fetched (e.g. daily, hourly) |
| fields_collected | List of attributes stored or used |
| personal_data | Whether personal data may be involved (yes/no) |
| storage_in_git_allowed | Whether raw or derived data may be committed |
| caching_allowed | Whether local caching is permitted by terms |
| fallback_behavior | What the application does when source is unavailable |

## Source-Specific Manifests

- **OSM (Geofabrik)**: See data/manifests/osm/README.md and docs/source-licensing.md. Acquisition: scripts/fetch_osm_azerbaijan.py; then services/network-import loads PBF into PostgreSQL (network_nodes, network_edges). Manifest in data/manifests/osm/manifest.json; network_import_manifest table stores import provenance. Refresh: manual or scheduled. No personal data. Raw PBF not in git. To run: make fetch-real-data, then pip install -e ./services/network-import and apply infrastructure/db/schema.sql, then make ingest-real-data.
- **Transit (GTFS)**: See services/transit-ingestion and docs/operator-integration-requirements.md. Baku Metro and BakuBus: permission_required until operator provides feed. No fabricated GTFS.
- **Weather (Open-Meteo)**: See services/weather-ingestion and docs/weather-integration.md. Public API. No personal data. Caching allowed per API terms.
- **Traffic**: See services/traffic-provider. Licensed provider (e.g. TomTom) requires credentials. When absent: configuration_required; no synthetic traffic.
- **Telemetry (Traccar)**: See services/telemetry and docs/telemetry-consent.md. Consent-based; personal data possible. No raw traces in git.
- **Events**: See services/event-ingestion and docs/event-sources.md. Public listings where ToS permit. No fabricated events in main path.
- **Energy context**: See services/energy-context and docs/energy-context.md. National or open data where licensing permits.

## Snapshot Metadata

When the platform serves recorded real snapshots (e.g. for demo when live is unavailable), each snapshot must include:

- source: source name from manifest
- captured_at: ISO timestamp of capture
- redaction_status: none, aggregated_only, anonymised
- license_status: ok, restricted, unknown

## Data provenance table

| Source family | Origin | Timestamp policy | Retention policy | Cache policy |
|---------------|--------|------------------|------------------|--------------|
| Network (OSM) | Geofabrik fetch + import | manifest fetched_at; import imported_at | Persistent in PostGIS; raw PBF not in repo | N/A |
| Weather | Open-Meteo | API response time | Per docs/data-retention.md | TTL per docs/data-refresh-policy.md |
| Transit | Operator or authorised feed | Feed published_at | Per retention and license | Per provider-refresh-matrix |
| Traffic | Licensed provider | Per API | Per retention | Short TTL; stale threshold |
| Telemetry | Traccar | Device timestamp | Consent and retention docs | Per docs/telemetry-consent.md |
| Events | Public listings | Event start/end | Per compliance notes | Per provider-refresh-matrix |
| Energy | National/open | As per source | Per docs/energy-context.md | Low frequency |

## Failure Behavior

When a source is unavailable or credentials are missing, the application must not silently substitute synthetic or invented data. It must:

- Return a clear status: unavailable, configuration_required, permission_required, or live/recorded_real_snapshot
- Expose this status in API responses and UI
- Document the gap and next required action (e.g. operator agreement, API key) in docs

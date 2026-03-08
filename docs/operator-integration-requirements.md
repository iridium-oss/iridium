# Operator Integration Requirements

This document states what is required to integrate real transit and mobility data from operators. It does not claim that any operator has agreed or that feeds exist. It defines the handoff for permission-based sources.

## Transit (GTFS and GTFS Realtime)

### Baku Metro

- **Desired**: GTFS static (stops, routes, trips, calendar) and optionally GTFS Realtime (trip updates, vehicle positions).
- **Current status**: permission_required. No public machine-readable feed is assumed. Integration will be enabled when the operator or authorised body provides a feed URL and terms.
- **Technical**: services/transit-ingestion supports GTFS static and GTFS Realtime. Provider registry entry for Baku Metro will move from permission_required to live when feed and credentials (if any) are configured.
- **Next step**: Obtain official or authorised GTFS feed and document URL, update cadence, and license in docs/source-licensing.md and provider config.

### BakuBus

- **Desired**: GTFS static and optionally GTFS Realtime for bus routes and services.
- **Current status**: permission_required. No fabricated feed.
- **Technical**: Same as above. Provider registry marks BakuBus as permission_required until a real feed is provided.
- **Next step**: Same as Baku Metro; operator or authorised body must provide feed and terms.

### Other Azerbaijani Operators

- Same pattern: add provider registry entry with status live, permission_required, or unavailable. Never invent a feed.

## Traffic (Licensed Segment Speed)

- **Desired**: Real-time or near-real-time segment speed or travel time (e.g. TomTom Traffic Flow).
- **Current status**: configuration_required. Application expects credentials (e.g. API key) via environment. When absent, traffic layer returns configuration_required; no synthetic traffic.
- **Next step**: Obtain contract and credentials; set TRAFFIC_PROVIDER, TRAFFIC_API_KEY (or equivalent) in .env; document in docs/source-licensing.md.

## Telemetry (Consent-Based GNSS)

- **Desired**: Consent-based device or fleet telemetry via Traccar (or similar) for aggregated speed and flow features.
- **Current status**: Optional. When Traccar is configured, ingestion runs; otherwise telemetry layer is unavailable. No synthetic traces in main path.
- **Next step**: Deploy Traccar; configure TRACCAR_HOST and credentials; ensure consent and privacy policy in place. See docs/telemetry-consent.md.

## Summary Table

| Source | Status | Required to enable |
|--------|--------|--------------------|
| OSM (Geofabrik) | Public; fetch script provided | Run fetch script; no permission |
| Open-Meteo weather | Public API | No key for basic use |
| Baku Metro GTFS | permission_required | Operator feed URL and terms |
| BakuBus GTFS | permission_required | Operator feed URL and terms |
| Traffic (e.g. TomTom) | configuration_required | API credentials and contract |
| Traccar telemetry | Optional | Traccar deployment and consent |
| Event listings | Depends on source | ToS-compliant access; see docs/event-sources.md |
| Energy context | Depends on source | License-compliant data; see docs/energy-context.md |

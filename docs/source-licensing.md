# Source Licensing and Terms

This document summarises licensing and terms for external data sources used or planned by IRIDIUM. It does not constitute legal advice. Operators and deployers must verify terms before use.

## OpenStreetMap and Geofabrik

- **Data**: OpenStreetMap contributors. License: ODbL (Open Database License). You must attribute and share-alike.
- **Geofabrik extracts**: Pre-built country/region extracts. Same ODbL. Terms: https://www.geofabrik.de/data/shapefiles.html and OSM legal.
- **Use in IRIDIUM**: Base road network, administrative boundaries, transport stops, cycling and pedestrian infrastructure. Processed network stored in PostgreSQL/PostGIS. Raw PBF files are not committed to the repository; fetch via script and store in infrastructure/raw-sources/osm or a gitignored cache.
- **Attribution**: Required in UI and documentation when displaying OSM-derived maps or data.

## Transit (GTFS)

- **GTFS static and Realtime**: License and terms are set by each transit operator. Baku Metro and BakuBus feeds (if and when provided) must be used according to operator terms.
- **IRIDIUM stance**: No GTFS is used in the main path until a real feed is obtained through official or authorised channels. Provider registry marks Baku as permission_required or unavailable. No fabricated feeds.

## Weather (Open-Meteo)

- **API**: Open-Meteo (https://open-meteo.com). Free for non-commercial and commercial use with attribution. No API key required for basic usage; rate limits apply.
- **Use**: Forecast and historical weather for Baku and Quba. Provenance and timestamp recorded.

## Traffic (Licensed Providers)

- **TomTom Traffic Flow**: Commercial product. Requires contract and API credentials. Use only when configured; otherwise application reports configuration_required.
- **Other providers**: Any licensed traffic provider must be documented here and in the provider adapter with license status.

## Event Listings

- **iTicket, CityLife, venue calendars**: Terms of service and robots.txt must be respected. Prefer official APIs or structured feeds. If scraping is used, it must be isolated, throttled, and documented in docs/compliance-notes.md.

## Energy Context

- **National or open data**: Use only where license and terms permit. Document source and license in docs/energy-context.md.

## Telemetry (Traccar)

- **Traccar**: Open source server. Device data is subject to consent and privacy policy. See docs/telemetry-consent.md and docs/privacy-notes.md. No raw personal traces in repository.

## General Rules

- Do not commit raw datasets to the repository unless the license explicitly permits it and the team has confirmed.
- All connectors must record source name, timestamp, and where applicable checksum of fetched file in provenance metadata.
- When in doubt, do not use; document the requirement and mark the source as permission_required or unavailable.

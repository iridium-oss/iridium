# AZ-local systems integration map

Canonical list of Azerbaijan and local systems that IRIDIUM targets for integration. Each row maps to provider registry entries and docs. Status is truthful: implemented, planned, or permission/configuration required.

## Transit core

| System | Scope | Registry id | Implementation status |
|--------|--------|-------------|------------------------|
| AYNA / Map AYNA | stop, route, tariff, carrier, stop list | bakubus_ayna | Implemented. getBusList, getBusById. Normalized route, stops, tariff (BakıKART fare note). |
| Baku Metro official | lines, stations, fare, schedules, operational notices | bakumetro_official, bakumetro_official_alerts | Implemented. Static network (lines, stations, fare, service window); alerts from official news. |
| BakuBus official | tickets, H1, news, alerts | bakubus_official_alerts | Implemented. Alerts from official news. H1/fare in lib/facts (pitch). |
| BakıKart | payment context, QR, validator, portal model | bakikart | Not implemented. Permission or partner required. Registry entry for tracking. |

## Event context

| System | Scope | Registry id | Implementation status |
|--------|--------|-------------|------------------------|
| iTicket | events, venues, event dates, category, venue address, QR/e-ticket context | iticket | Not implemented. Documented in event-sources.md. ToS and robots.txt must be respected. |

## Map and routing

| System | Scope | Registry id | Implementation status |
|--------|--------|-------------|------------------------|
| GoMap API | search, region lookup, route XML | gomap_api | Not implemented. Add when API or partnership available. |
| 2GIS Public Transport API | route building, schedule-aware route options | twogis_public_transport | Adapter exists. Requires IRIDIUM_TWOGIS__API_KEY when enabled. |
| Yandex observed transport | stop-level arrival cards and ETA semantics | yandex_transport_observed | Implemented. Public web observed; not operator GTFS-RT. |
| Yandex observed traffic | traffic context only | yandex_traffic_context | Adapter exists. Traffic context only; status from get_traffic_context_status. |

## Weather and EO

| System | Scope | Registry id | Implementation status |
|--------|--------|-------------|------------------------|
| Open-Meteo | forecast, historical weather, geocoding | open_meteo | Implemented. Forecast and current; historical API available, persistence not wired. |
| Copernicus STAC | Sentinel-2 scene search | copernicus_stac | Implemented. Primary catalog path. |
| Sentinel Hub | rendering and process API | sentinel_hub | Optional. Configuration when IRIDIUM_EO__SENTINEL_HUB_INSTANCE_ID set. |
| Earth Search | fallback STAC catalog | earth_search_stac | Implemented. Fallback for Sentinel-2 L2A. |

## Cross-references

- Provider registry: GET /api/v1/system/providers. See docs/provider-registry.md.
- Transit: docs/baku-transit-integration.md, docs/transit-data-governance.md.
- Events: docs/event-sources.md.
- EO: docs/sentinel2-integration.md, docs/eo-limitations.md.

# Baku Realtime Supplementary Sources - Final Report

## New real sources added

| Provider | Type | What it provides |
|----------|------|------------------|
| bakubus_official_alerts | Official website | Alerts from BakuBus news/notifications page (title, link, published_at). source_status=official_alerts_only. |
| bakumetro_official_alerts | Official website | Alerts from Baku Metro news/updates page. source_status=official_alerts_only. |
| yandex_transport_observed | Public web observed | PredictedArrival (when minute hints in HTML), StopRealtimeStatus. source_status=public_web_observed. Never labeled as official GTFS Realtime. |
| yandex_metro_operational | Public web observed | MetroOperationalNotice, MetroRoutingConstraint (e.g. closed station hints). source_status=public_web_operational_context. |
| yandex_traffic_context | Web observed / licensed | RoadTrafficContext. Status: web_observed | licensed_api | unavailable. Licensed mode when YANDEX_TRAFFIC_API_KEY set. |
| twogis_public_transport | Licensed API | TransitPartnerRouteResult (duration, transfer_count, route variants). source_status=licensed_partner. Requires TWOGIS_API_KEY. |
| moovit_partner | Partner required | Interface and config only. source_status=partner_required. Placeholder for route planning, arrivals, alerts when credentials added. |

## Gaps filled

- **Service alerts**: Official BakuBus and Baku Metro pages provide alert-like content; merged by priority and exposed at GET /api/v1/transit/alerts.
- **Predicted arrivals**: Yandex Baku transport/stop pages can yield minute hints; normalized to PredictedArrival with clear public_web_observed status.
- **Operational context**: Yandex Metro Baku page can yield closed-station/entrance hints; normalized to MetroOperationalNotice and MetroRoutingConstraint.
- **Route planning**: 2GIS Public Transport API (when key set) and Moovit (when configured) provide route alternatives and ETA enrichment; not operator ground truth.
- **Traffic context**: Status and placeholder for Yandex traffic; licensed mode when API key set.

## What remains unavailable

- Official BakuBus or Baku Metro GTFS Realtime (trip updates, vehicle positions).
- Machine-readable official alert feed from operators.
- Reliable, stable stop-level predictions from an official or documented API (Yandex pages are often JS-rendered; extraction may be empty).

## Official vs public-web vs licensed

- **Official**: bakubus_official_alerts, bakumetro_official_alerts (official site HTML; not machine-readable API).
- **Public-web observed**: yandex_transport_observed, yandex_metro_operational (public pages; not official operator feed).
- **Licensed**: twogis_public_transport (2GIS API), moovit_partner (when configured), yandex_traffic_context (when API key set).

## User-visible functionality

- Dashboard Transit page shows: source status badges (official, public-web observed, licensed partner, unavailable), official alerts from BakuBus and Metro, predicted arrivals where observed, provider list and readiness. No fake vehicle positions or fake ETAs.
- API: GET /transit/alerts, /transit/predicted-arrivals, /transit/realtime-observations, /transit/provider-priority, /transit/source-status with truthful metadata per item.

## What still requires operator agreement

- Official GTFS or GTFS Realtime from BakuBus or Baku Metro for authoritative timetables and realtime trip/vehicle data.
- Any use of scraped or observed data must comply with site terms and robots.txt; operator partnership is preferred for production-grade realtime.

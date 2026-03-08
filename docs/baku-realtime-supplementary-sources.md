# Baku Realtime and Supplementary Data Sources

This document describes the real, non-fabricated supplementary sources used for transit realtime and operational data in Baku when official GTFS Realtime or operator-issued machine-readable feeds are unavailable.

## Core rule

No invented realtime feeds. All sources are either publicly accessible, officially published, or commercially licensable. Public but non-official developer APIs are modeled explicitly (e.g. public_web_observed, licensed_partner).

## Sources integrated

### Official alert sources

| Provider | Source | Machine-readable | Data contributed |
|----------|--------|------------------|------------------|
| bakubus_official_alerts | BakuBus official site (news/notifications) | No (HTML) | Alerts: title, link, published_at; source_status=official_alerts_only |
| bakumetro_official_alerts | Baku Metro official site (news/updates) | No (HTML) | Alerts: title, link, published_at; source_status=official_alerts_only |

Parsing is based on link and text extraction from HTML. Page structure may change; parser may return empty. No fabricated alerts.

### Public web observed

| Provider | Source | Machine-readable | Data contributed |
|----------|--------|------------------|------------------|
| yandex_transport_observed | Yandex Maps Baku transport / stop pages | No (HTML, often JS-rendered) | PredictedArrival (when minute hints found), StopRealtimeStatus; source_status=public_web_observed |
| yandex_metro_operational | Yandex Metro Baku page | No (HTML) | MetroOperationalNotice, MetroRoutingConstraint; source_status=public_web_operational_context |

Never labeled as official operator GTFS Realtime. Provenance includes page URL, observed_at, scrape method, parser version, confidence note.

### Traffic context

| Provider | Source | Status | Data contributed |
|----------|--------|--------|------------------|
| yandex_traffic_context | Yandex traffic / routing | web_observed / licensed_api / unavailable | RoadTrafficContext, SegmentCongestionLevel when implemented; status from get_traffic_context_status() |

When YANDEX_TRAFFIC_API_KEY is set, status is licensed_api. Otherwise unavailable (web-observed traffic layer not implemented).

### Licensed partner APIs

| Provider | Source | Machine-readable | Data contributed |
|----------|--------|------------------|------------------|
| twogis_public_transport | 2GIS Public Transport API | Yes (documented API) | TransitPartnerRouteResult: total_duration, transfer_count, route variants, schedules when returned; source_status=licensed_partner. Requires TWOGIS_API_KEY. |
| moovit_partner | Moovit developer/partner products | Yes (when configured) | Interface only; source_status=partner_required. Route planning, arrival predictions, service alerts when credentials added. |

Used for route-planning and ETA enrichment; not operator-issued ground truth.

## What remains unavailable

- Official BakuBus or Baku Metro GTFS Realtime (trip updates, vehicle positions).
- Machine-readable official alert feed from operators.
- Reliable stop-level predictions from a stable official or documented API (Yandex pages are JS-heavy; extraction may be empty).

## Legal and operational caution

- Official site parsing: respect robots.txt and rate limits; do not overload servers.
- Yandex: public pages; do not represent as official operator data; observe terms of use.
- 2GIS: use under API terms and key agreement.
- Moovit: partner agreement required for production use.

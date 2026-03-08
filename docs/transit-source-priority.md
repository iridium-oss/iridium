# Transit Source Priority Policy

Source priority defines which provider is preferred when multiple sources contribute the same kind of data. Lower rank means higher priority.

## Alerts

1. bakubus_official_alerts (official BakuBus pages)
2. bakumetro_official_alerts (official Baku Metro pages)
3. yandex_transport_observed
4. yandex_metro_operational
5. moovit_partner

Official operator pages are preferred over public-web observed and licensed partner sources. Merge and deduplication use alert_id; first occurrence by priority wins.

## Predicted arrivals

1. official_gtfs_realtime (if ever added)
2. yandex_transport_observed (public web observed)
3. moovit_partner
4. twogis_public_transport

Official machine-readable feed would take precedence. Today only public-web observed (Yandex) or licensed partners can contribute; never fabricated.

## Route planning

1. otp_gtfs (repository-generated or official GTFS with OpenTripPlanner)
2. twogis_public_transport (2GIS Public Transport API)
3. moovit_partner
4. yandex_licensed_routing (when configured)

When exact stop_times are not available, OTP timetable routing is not supported; 2GIS or Moovit can still provide route alternatives and duration from their APIs.

## Implementation

- `transit_ingestion.provenance.priority`: get_alert_priority_order(), get_predicted_arrival_priority_order(), get_route_planning_priority_order(), merge_alerts_by_priority().

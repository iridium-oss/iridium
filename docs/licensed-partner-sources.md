# Licensed Partner Sources

Transit data from commercial or partner APIs (2GIS, Moovit, Yandex business routing) is classified as **licensed** and used for route-planning and ETA enrichment, not as operator-issued ground truth.

## 2GIS Public Transport API

- **source_family**: licensed_api
- **source_status**: licensed_partner
- **Configuration**: TWOGIS_API_KEY environment variable.
- **Data**: Route alternatives between points, total_duration, transfer_count, route variants, schedules when returned. Documented developer API.
- **Use**: Route-planning and ETA enrichment. Not operator GTFS.

## Moovit partner

- **source_family**: licensed_api
- **source_status**: partner_required
- **Configuration**: MOOVIT_PARTNER_API_KEY (and optional base URL). Credentials not assumed.
- **Data**: Interface defined for route planning, arrival predictions, service alerts. Implementation placeholder until partner agreement and credentials.
- **Use**: Future-ready; add credentials without redesign.

## Yandex traffic / routing

- **yandex_traffic_context**: When YANDEX_TRAFFIC_API_KEY is set, status is licensed_api. Otherwise unavailable. Road traffic context for Baku; not implemented beyond status and placeholder context.

## Rules

- Never represent licensed partner output as official operator feed.
- Every record includes source_provider, source_family, source_status.
- Route planning panels may use licensed providers when configured; UI must indicate "licensed partner" or equivalent.

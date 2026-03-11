# Provider registry

The API exposes a unified provider registry for all external APIs and data sources. Each provider has a stable id, source_family, source_status, capabilities, and optional verification.

## Endpoints

- **GET /api/v1/system/providers**: List all providers with capabilities and notes. No live check.
- **GET /api/v1/system/providers/{provider_id}**: Single provider entry. 404 if unknown.
- **GET /api/v1/system/providers/{provider_id}/health**: Current health/validation status. Runs verification.
- **POST /api/v1/system/providers/{provider_id}/verify**: Run verification (e.g. sample request). Returns validation_status.
- **GET /api/v1/system/integrations/status**: Aggregate by domain. No live checks.
- **GET /api/v1/system/integrations/report**: Full report with verification result per provider. Runs live checks; may be slow.

## Provider fields

- **id**: Stable identifier (e.g. open_meteo, copernicus_stac, bakubus_ayna).
- **display_name**: Human-readable name.
- **source_family**: official_website, public_api, public_undocumented, public_web_observed, licensed_partner, stac_catalog, etc.
- **source_status**: public_api, official_alerts_only, public_web_observed, configuration_required, permission_required, etc.
- **domain**: weather, transit, earth_observation, traffic, telemetry, network.
- **required_env_vars**: Environment variables required when the provider is enabled (e.g. IRIDIUM_TWOGIS__API_KEY).
- **capabilities**: supports_search, supports_metadata, supports_tiles, supports_routing, supports_alerts, supports_realtime, supports_historical, supports_analytics, supports_auth, supports_web_observation.
- **validation_status**: working, partially_working, configuration_required, permission_required, unavailable, not_checked, etc.

## Verification

Verification runs a minimal live check where implemented (e.g. Open-Meteo fetch, STAC root request, transit fetch). Missing credentials yield configuration_required. Unknown provider or no handler yields not_checked. Results are not cached; each health or verify call runs the check.

## Environment and credentials

- **Open-Meteo**: No key. Enabled by default.
- **Copernicus STAC / Earth Search STAC**: No auth for search. Optional CDSE auth: IRIDIUM_EO__CDSE_USERNAME/PASSWORD or IRIDIUM_EO__CDSE_CLIENT_ID/SECRET (or legacy CDSE_USERNAME, CDSE_PASSWORD, CDSE_CLIENT_ID, CDSE_CLIENT_SECRET) for higher limits; Bearer token used when set.
- **Sentinel Hub**: Optional. Set IRIDIUM_EO__SENTINEL_HUB_INSTANCE_ID; for token-based Process API also set IRIDIUM_EO__SENTINEL_HUB_CLIENT_ID and IRIDIUM_EO__SENTINEL_HUB_CLIENT_SECRET (or SENTINEL_HUB_CLIENT_ID, SENTINEL_HUB_CLIENT_SECRET). Verify endpoint checks token acquisition.
- **2GIS**: IRIDIUM_TWOGIS__API_KEY or legacy TWOGIS_API_KEY. Set IRIDIUM_PROVIDERS__TWOGIS_ENABLED=true to enable; GET /api/v1/transit/partner-routes uses 2GIS when key is present.
- **Moovit**: IRIDIUM_MOOVIT__API_KEY or MOOVIT_API_KEY; IRIDIUM_MOOVIT__BASE_URL or MOOVIT_BASE_URL. Set IRIDIUM_PROVIDERS__MOOVIT_ENABLED=true to enable. Partner-routes endpoint uses Moovit when configured.
- **GoMap**: IRIDIUM_GOMAP__API_KEY or GOMAP_API_KEY; GOMAP_ALLOWED_SERVER_IP optional. No adapter yet; registry entry and settings only.
- **Traccar**: TRACCAR_HOST and credentials when telemetry is enabled.

At startup, IRIDIUM_* credentials are propagated to legacy env names (e.g. TWOGIS_API_KEY) so adapters that read env directly receive the values. The application does not crash if an optional provider is misconfigured; endpoints return explicit status.

## Frontend

- **Dashboard > Providers**: Lists all providers, capability badges, source status, and a Verify button per provider.
- **Dashboard > System status**: Shows integrations summary and link to Providers.

## AZ-local systems map

For the canonical list of Azerbaijan and local systems (AYNA, Baku Metro, BakuBus, BakıKart, iTicket, GoMap, 2GIS, Yandex, Open-Meteo, EO), see docs/az-local-systems-integration-map.md.

## See also

- docs/az-local-systems-integration-map.md: AZ-local systems integration map.
- docs/provider-matrix.md: Domain-level provider matrix.
- docs/implementation-status.md: What is implemented per backend and service.

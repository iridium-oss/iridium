# Public vs Permissioned Sources

Clear separation between sources that are publicly usable and those that require permission or credentials.

## Public (No Key or Permission Required)

- **OpenStreetMap (Geofabrik)**: Azerbaijan extract. ODbL; attribution required. Fetch via script; no account.
- **Open-Meteo**: Weather API. Free; attribution required. No API key for basic use.

## Permission or Credentials Required

- **Baku Metro GTFS**: permission_required. No public feed assumed. Operator or authorised body must provide feed and terms.
- **BakuBus GTFS**: permission_required. Same as above.
- **TomTom Traffic Flow** (or equivalent): configuration_required. Commercial; API key and contract required.
- **Traccar**: Optional. Deployer runs Traccar; credentials and consent required for device data.
- **Event listings**: Depends on source. Some require API key or ToS compliance; no scraping without compliance notes.
- **Energy context**: Depends on dataset licence. Document in docs/energy-context.md.

## Behaviour When Not Enabled

When a permissioned or configured source is not enabled, the application does not substitute synthetic or invented data. It returns a clear status (configuration_required, permission_required, or unavailable) in API and UI. See docs/real-data-mode.md and docs/provider-matrix.md.

# Traffic Provider

Abstraction for real-time or near-real-time segment speed or travel time. When credentials (e.g. TomTom Traffic Flow API key) are configured and adapter is implemented, returns live or recorded_real_snapshot. When absent, returns configuration_required; no synthetic traffic in main path.

## Configuration

- TRAFFIC_PROVIDER: e.g. tomtom
- TRAFFIC_API_KEY or TOMTOM_API_KEY: API key when using licensed provider

See docs/operator-integration-requirements.md and docs/source-licensing.md.

# Telemetry and Consent

IRIDIUM may ingest GNSS telemetry from consent-based device or fleet tracking (e.g. via Traccar). This document describes the consent and privacy requirements. It does not constitute legal advice.

## Principles

- Telemetry must be collected only with valid consent and a clear privacy policy.
- Device or vehicle IDs should be pseudonymous where possible; document re-identification risk and mitigation.
- Retention must be minimal and defined; see docs/data-retention.md.
- No raw personal traces are committed to the repository. Test fixtures must be synthetic or fully de-identified and legally safe to store.

## Traccar Integration

- **Role**: Traccar is an open source fleet/device tracking server. When configured, IRIDIUM can consume position and trip data from Traccar for aggregated features (e.g. segment speeds, flow proxies).
- **Configuration**: TRACCAR_HOST, TRACCAR_CREDENTIALS (or equivalent) in .env. When not set, telemetry layer is unavailable; no synthetic traces.
- **Data flow**: Only aggregated or derived features (e.g. segment-level speed) should be used in the digital twin or forecasting where personal data must be minimised. Raw positions are not stored in IRIDIUM beyond what is required for aggregation and retention policy.
- **Consent**: Operator or deployer must ensure that all devices or vehicles reporting to Traccar have consented (e.g. driver consent, fleet policy) and that the privacy policy is available to data subjects.

## Developer Mode

- For local development, developers may connect their own opted-in devices or approved test trackers to Traccar. No production or third-party data without agreement.
- Recorded trip ingestion for testing: only if the trace is consented, de-identified, and legally safe to store. Prefer synthetic fixtures for unit tests.

## Privacy notes and sensitive data awareness

IRIDIUM can integrate mobility related data sources. Depending on configuration, deployments may handle data that is sensitive. This repository baseline avoids committing raw sensitive data and provides guidance for safer handling.

### What is sensitive

Treat the following as sensitive by default:

- **Device level telemetry**: GNSS traces, device identifiers, per trip traces, and any raw logs that can be linked to an individual.
- **Credential material**: API keys, passwords, tokens, session cookies, and connection strings containing secrets.
- **Partner feeds**: Licensed or permission required datasets where terms restrict redistribution or caching.

### Repository rules

- Do not commit `.env` files or secret material.
- Do not commit raw telemetry or raw provider payload captures.
- Prefer aggregated or anonymised derived datasets for tests and demos.

### Retention and caching guidance

- Default to short retention for cached external payloads unless terms permit longer storage.
- Avoid caching payloads that include identifiers or fine grained traces.
- When recorded snapshots are used for demos, store only the minimum necessary fields and include provenance and redaction status metadata.

### Provenance without unsafe exposure

Provenance should describe the source and capture time without embedding raw upstream payloads:

- provider id and source family
- source status and access type
- observed at or fetched at timestamps
- license or terms reference
- validation notes and confidence signals where applicable

# Privacy Notes

IRIDIUM is designed to support privacy-preserving deployment. This document states design choices and operational notes. It does not constitute legal advice. Deployers are responsible for compliance with applicable law.

## Design Principles

- **Federated learning**: Raw personal data does not leave participant nodes; only model updates (or encrypted parameters) are shared. This reduces centralisation of personal data but does not by itself guarantee legal compliance.
- **No centralisation of raw mobility traces**: The platform does not require raw GNSS traces or trip records to be stored centrally. Telemetry integration (e.g. Traccar) is consent-based and may use pseudonymous device IDs with strict retention.
- **Transit and network data**: GTFS and OSM-derived data are not personal data. Operator terms still apply.
- **Traffic data**: Licensed traffic providers typically supply aggregated segment speeds; ensure provider contract and data handling align with deployment jurisdiction.
- **Event data**: Public event listings are not personal data; respect source terms of service.

## Telemetry and GNSS

- **Consent**: Any device or vehicle telemetry must be collected only with valid consent and a clear privacy policy. See docs/telemetry-consent.md.
- **Pseudonymous IDs**: Use device or vehicle IDs that do not directly identify individuals; document how re-identification could occur and mitigate.
- **Retention**: Minimum necessary; purge when no longer needed for the consented purpose. See docs/data-retention.md.
- **No raw traces in repository**: Raw GNSS traces must never be committed to the repository. Test fixtures must be synthetic or fully de-identified and legally safe.

## Data Status in UI and API

The application exposes data status (e.g. live, recorded_real_snapshot, unavailable, configuration_required, permission_required). Do not present unavailable or permission-required sources as if they contained real user data. When a source is unavailable, say so explicitly.

## Operator and Third-Party Data

When integrating with transit operators or other third parties, data sharing and processing must be governed by agreement. Document requirements in docs/operator-integration-requirements.md. Do not assume permission to store or process personal data from operators without explicit agreement.

## Regulatory Context

Azerbaijan and other jurisdictions may have data protection or sector-specific rules. The architecture is designed to support privacy-aware deployment; deployers must obtain their own legal and compliance advice.

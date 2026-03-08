# Compliance Notes

Operational and legal compliance considerations for IRIDIUM data connectors. This is not legal advice. Deployers must ensure their use complies with applicable law and third-party terms.

## Web Scraping and APIs

- When ingesting from websites or APIs, respect robots.txt, terms of service, and rate limits.
- Isolate any scraping behind throttling and clear documentation. Prefer official APIs or licensed feeds.
- If a source explicitly prohibits automated access, do not integrate without permission. Mark source as permission_required in provider registry.

## Data Protection

- Personal data (e.g. device positions, trip traces) must be handled per consent and privacy policy. See docs/privacy-notes.md and docs/telemetry-consent.md.
- No central storage of raw personal mobility data beyond what is necessary and consented. Federated design supports this; deployers remain responsible for compliance.

## Operator and Third-Party Agreements

- Transit (GTFS), traffic, and other operator data require agreement where not publicly licensed. See docs/operator-integration-requirements.md.
- Do not assume permission to store, process, or redistribute third-party data without explicit agreement or license.

## Attribution and Licensing

- OSM: Attribution required (ODbL). See docs/source-licensing.md.
- Open-Meteo: Attribution per API terms.
- Other sources: Document in docs/source-licensing.md and provider manifest.

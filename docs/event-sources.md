# Event Sources

IRIDIUM uses real public event listings as demand-signal features where legally and technically feasible. No fabricated event records are used in the main application path.

## Candidate Sources

- **iTicket**: Ticketing and events. Use only if API or authorised feed is available. Respect robots.txt and terms of service.
- **CityLife**: Event listings. Same as above.
- **Official venue calendars**: Where machine-readable or API access is provided and terms permit.

## Requirements

- Respect robots.txt, terms of service, and rate limits.
- Prefer public APIs or structured feeds over scraping. If scraping is required, isolate behind clear compliance notes and throttling; see docs/compliance-notes.md.
- Normalise events into: title, venue, start_time, end_time, category, source, source_url, confidence.
- Use events only as demand-signal features, not as definitive attendance counts.
- When no real source is configured or available, event layer returns unavailable; no synthetic events in main path.

## Implementation

- **Service**: services/event-ingestion. Provider adapters per source; status in provider registry (live, permission_required, unavailable).
- **Provenance**: Each event record includes source and source_url; fetched_at recorded.

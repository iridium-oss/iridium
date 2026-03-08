# Public Web Observed Data

Data obtained by observing public web pages (e.g. Yandex Maps Baku transport or metro pages) is classified as **public web observed** and must never be represented as official operator or GTFS Realtime data.

## Classification

- **source_family**: public_web
- **source_status**: public_web_observed or public_web_operational_context

## Providers

- **yandex_transport_observed**: Baku transport and stop pages. Extracted: stop-level predicted arrival hints (e.g. "5 min" in HTML), stop status. Many pages are JS-rendered; extraction may return empty. Provenance: page URL, observed_at, scrape method, parser version, confidence note.
- **yandex_metro_operational**: Yandex Metro Baku. Extracted: closed-station or entrance-restriction hints from HTML. Normalized to MetroOperationalNotice, MetroRoutingConstraint.

## Constraints

- Do not label as official operator feed or GTFS Realtime.
- Include provenance (URL, observed_at, method, confidence) on every record.
- Frontend and API must show "public-web observed" (or equivalent) so users know the source.
- No fake vehicle positions or invented ETAs; only what is extracted from the page.

## Limitations

- HTML structure changes can break parsers.
- JS-rendered content may not be visible to server-side fetch; extraction may be empty.
- No legal guarantee of scraping rights; use responsibly and in line with site terms.

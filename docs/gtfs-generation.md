# GTFS Generation

IRIDIUM can build a GTFS Static package from normalized BakuBus and Baku Metro data. The output is **repository-generated** from official and public sources; it is **not** operator-issued.

## Label

All generated GTFS is labeled: "Repository-generated from official and public sources. Not operator-issued."

## What is generated when data is available

- **agency.txt**: From TransitAgency (Baku Metro, BakuBus).
- **routes.txt**: From TransitRoute (metro lines, bus routes).
- **stops.txt**: From TransitStop. Coordinates included only when present (e.g. AYNA stops; metro after OSM resolution).
- **shapes.txt**: From TransitShapePoint (e.g. AYNA flowCoordinates).
- **trips.txt** / **stop_times.txt**: Only when exact trip-level timetable data is defensible. Currently omitted for both BakuBus and Baku Metro (no fabricated timetable).
- **calendar.txt** / **calendar_dates.txt**: Only if justified by source data.
- **fare_attributes.txt**: Only if justified (e.g. basic fare from AYNA tariff or metro official page).

## What is not fabricated

- No invented stop coordinates for metro until OSM resolution (and validation) provides them.
- No invented stop_times or trips when exact schedules are not available.
- No claim that the GTFS is the official operator feed.

## Export directory

- Feed export path: `transit_ingestion.storage.get_feed_export_dir()`. Default directory: `feed_export/` (or set `IRIDIUM_GTFS_OUTPUT_DIR`). When `build_gtfs_static(snapshot, output_dir=None)`, the builder uses this path. It writes agency.txt, routes.txt, stops.txt, shapes.txt (when present), and README.txt. README states the label and what is included or omitted.

## Validation and OTP preparation

- Validation checks: canonical schema validation; optional GTFS static validation (e.g. feedvalidator) when run externally.
- Provider capability matrix and readiness report answer: static stop discovery, route visualization, transfer graph, timetable routing. Timetable routing is false when stop_times are not trustworthy.
- For production-grade OpenTripPlanner: exact stop_times, complete coordinates, and optionally realtime feeds are still needed; the readiness report lists missing_for_otp.

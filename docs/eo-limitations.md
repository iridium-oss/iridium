# Earth observation limitations

## Scope

Sentinel-2 in IRIDIUM is used only as **near-recent earth observation context**. The following limitations apply and must be reflected in UI and API.

## What EO is not

- **Not realtime traffic**: Satellite imagery is not live traffic flow or vehicle counts.
- **Not realtime transit**: It does not show bus or metro positions or schedules.
- **Not thermal surface temperature**: Sentinel-2 has no thermal band; do not infer ground or surface temperature from it.
- **Not minute-level operational truth**: Revisit is on the order of days; use for environmental and planning context only.

## Provenance and status

- Every EO-derived output must expose: provider, acquisition date, cloud cover when available, and whether the layer is direct imagery or a derived index.
- Source status (live, unavailable, cached, etc.) must be shown so users know when data is missing or stale.
- A clear misuse warning must be shown where appropriate: satellite context is not realtime transport telemetry.

## Indices

- NDVI, NDWI, NDBI are standard band-math indices. They are defensible for vegetation, water-sensitive, and built-up context but are not calibrated to a specific product claim without validation.
- AOI statistics (mean/min/max over an area) are placeholder in the current implementation; full implementation would require raster access and processing.

## Tiles and rendering

- True-color and index visualization may require a tile or Process API (e.g. Sentinel Hub) when configured. Without it, the map shows basemap and AOI bounds only; layer descriptors and provenance are still returned.

## Data availability

- Scenes depend on provider availability (Copernicus, Earth Search). If both are unreachable or return no results, the API returns empty scenes with explicit source_status.

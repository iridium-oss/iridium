# Earth Observation (Sentinel-2) service

Sentinel-2 imagery integration for IRIDIUM. Provides STAC-based scene search, index generation (NDVI, NDWI, NDBI), and layer descriptors for the frontend. Not realtime traffic or transit data.

## Primary provider

- Copernicus Data Space Ecosystem STAC (`https://stac.dataspace.copernicus.eu/v1/`)

## Fallback

- Earth Search STAC (`https://earth-search.aws.element84.com/v1`)

## Optional

- Sentinel Hub Process API or OGC for rendering when configured.

## Structure

- `earth_observation/sentinel2/providers/` – STAC provider adapters
- `earth_observation/sentinel2/search/` – search by bbox, polygon, preset, date, cloud
- `earth_observation/sentinel2/processing/` – index formulas and layer generation
- `earth_observation/sentinel2/indices/` – NDVI, NDWI, NDBI descriptors
- `earth_observation/sentinel2/caching/` – search result cache
- `earth_observation/sentinel2/manifests/` – area presets (e.g. Baku)

## Credentials

- Copernicus: optional; unauthenticated search may have limits.
- Earth Search: no auth required.
- Sentinel Hub: set `IRIDIUM_EO__SENTINEL_HUB_INSTANCE_ID` and instance secret when using Process API.

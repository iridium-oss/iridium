# Sentinel-2 integration

Sentinel-2 is integrated into IRIDIUM as a real earth-observation context layer. It is not used for realtime traffic, transit positions, or minute-level operational data.

## What Sentinel-2 adds

- **Spatial intelligence**: Urban footprint, green cover, water presence, land-use and built-up context around mobility corridors.
- **District-level context**: Environmental context for mobility equity and resilience analysis.
- **Corridor context**: Vegetation (NDVI), water-sensitive (NDWI), and built-up (NDBI) indices for planning narratives.

## What it does not add

- Realtime traffic or transit feeds.
- Live vehicle or passenger positions.
- Thermal surface temperature (Sentinel-2 does not provide thermal bands).
- Minute-level operational truth.

## How it is searched

- **Primary**: Copernicus Data Space Ecosystem STAC (`https://catalogue.dataspace.copernicus.eu/stac`). STAC search by bbox, datetime range, and cloud cover.
- **Fallback**: Earth Search STAC (`https://earth-search.aws.element84.com/v1`), collection `sentinel-2-l2a`.
- Search supports bbox, polygon (via bbox), city/district presets (e.g. Baku), date range, and cloud cover filter.
- Results are cached with a configurable TTL (`IRIDIUM_EO__SEARCH_CACHE_TTL_SECONDS`).

## How it is processed

- **Indices**: NDVI (B08, B04), NDWI (B03, B08), NDBI (B11, B08). Formulas are documented in code and in docs.
- **Composites**: True-color (B04, B03, B02) and false-color descriptors are available; tile URLs require a rendering service (e.g. Sentinel Hub Process API) when configured.
- **AOI statistics**: Placeholder for mean/min/max over a bounding box; full implementation would use raster clip and band math.

## How it is shown in the product

- **Dashboard**: Satellite context page with area preset, scene list, layer toggle (true color, NDVI, NDWI, NDBI), map with AOI bounds, and provenance drawer.
- **System status**: EO provider status and data_status on the status page.
- **Methodology**: EO use and limitations described in the methodology section.
- Every layer exposes source provider, acquisition date, cloud cover, and a misuse warning.

## Backend and frontend wiring

- **API**: `/api/v1/eo/status`, `/api/v1/eo/providers`, `/api/v1/eo/areas`, `/api/v1/eo/scenes/search`, `/api/v1/eo/scenes/{scene_id}`, `/api/v1/eo/layers/true-color`, `/api/v1/eo/layers/ndvi`, `/api/v1/eo/layers/ndwi`, `/api/v1/eo/layers/ndbi`, `/api/v1/eo/stats`, `/api/v1/eo/provenance`.
- **Settings**: `IRIDIUM_EO__ENABLED`, `IRIDIUM_EO__PREFER_COPERNICUS`, `IRIDIUM_EO__COPERNICUS_STAC_URL`, `IRIDIUM_EO__EARTH_SEARCH_STAC_URL`, `IRIDIUM_EO__SEARCH_CACHE_TTL_SECONDS`, optional Sentinel Hub instance and base URL.
- **Frontend**: Next.js dashboard route `/dashboard/satellite`, Leaflet map, layer controls, provenance modal, area/date and source-status display.

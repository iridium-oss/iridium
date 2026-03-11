# Earth observation architecture

## Overview

IRIDIUM uses Sentinel-2 as an earth-observation (EO) context layer. The architecture is provider-agnostic at the API layer and uses STAC as the primary search path.

## Components

### Services

- **earth-observation** (Python package `earth_observation`): Sentinel-2 providers, search orchestration, index descriptors, caching, area presets.
  - `sentinel2/providers/`: Copernicus STAC, Earth Search STAC, base protocol.
  - `sentinel2/search/`: Search by bbox or preset, provider fallback.
  - `sentinel2/indices/`: NDVI, NDWI, NDBI formulas and layer descriptors.
  - `sentinel2/processing/`: Overlay descriptors, AOI stats placeholder.
  - `sentinel2/caching/`: In-memory cache for search results and layer descriptors.
  - `sentinel2/manifests/`: Area presets (e.g. Baku, corridor sample).

### Schemas (packages/schemas)

- **earth_observation**: EOScene, EOSceneMetadata, EOSceneSearchResult, EOBandAsset, EOIndexLayer, EOTileLayer, EOOverlayDescriptor, EOProcessingJob, EOAreaPresetDefinition, EOSourceStatus. All include source_provider, source_status, acquired_at, cloud_cover when available, confidence_note, validation_note.

### API (apps/api)

- **eo** router under `/api/v1`: status, providers, areas, scenes/search, scenes/{id}, layers/true-color, layers/ndvi, ndwi, ndbi, stats, provenance. All responses include source status and provenance fields.

### Frontend (apps/web)

- **Satellite context page**: Map (Leaflet), scene list, layer toggles, acquisition date and cloud cover, provenance drawer, source-status badges.
- **Status page**: EO status and providers.
- **Methodology**: EO section with limitations and references.

## Data flow

1. User selects area (preset or bbox) and optional date range and cloud filter.
2. API calls search orchestration; primary provider (Copernicus) is tried, then fallback (Earth Search).
3. Search results are normalized to EOScene and optionally cached.
4. User selects a scene; layer descriptors (true-color, NDVI, NDWI, NDBI) are built from scene metadata and index formulas.
5. Provenance and limitations are exposed on every response and in the UI.

## Credentials and configuration

- Copernicus: optional auth; unauthenticated search may have rate limits.
- Earth Search: no auth.
- Sentinel Hub Process API: optional; set `IRIDIUM_EO__SENTINEL_HUB_INSTANCE_ID` and base URL when using for tile rendering or statistics.

## Caching and performance

- Scene search results: in-memory cache with TTL (default 5 minutes).
- Layer descriptors: in-memory cache (default 10 minutes).
- No large rasters stored in git; pull-on-demand via STAC and optional Process API.

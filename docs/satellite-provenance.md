# Satellite provenance

Every satellite-derived output in IRIDIUM must disclose provenance and intended use. This document describes the provenance model for earth observation (EO) layers.

## Required fields

For every EO scene or layer the following must be exposed (in API and where relevant in UI):

- **source_provider**: Identifier of the catalog or service (e.g. copernicus_stac, earth_search_stac).
- **source_family**: High-level source type (e.g. stac_catalog).
- **source_status**: Availability status (live, unavailable, cached, configuration_required, etc.).
- **acquired_at**: Scene acquisition datetime (UTC) when available.
- **processed_at**: When the product was processed, if relevant for derived layers.
- **cloud_cover**: Cloud cover percentage when provided by the catalog.
- **bbox or geometry**: Spatial extent of the scene.
- **confidence_note**: Short note on confidence or interpretation.
- **validation_note**: Non-sensitive validation or quality note when applicable.

## Layer-specific disclosure

- **Imagery (true-color, false-color)**: State that it is direct or composite imagery; acquisition date and cloud cover; not realtime.
- **Index layers (NDVI, NDWI, NDBI)**: State formula and bands; state that it is a derived index for environmental context; include misuse warning that it is not traffic or transit data.

## Misuse warning

A standard warning is included where appropriate: satellite context is not realtime traffic, transit positions, or minute-level operational data; it is for environmental and planning context only.

## API and UI

- **API**: `/api/v1/eo/provenance?scene_id=...` returns full provenance for a scene; layer endpoints include source_provider, source_status, acquired_at, cloud_cover, and misuse_warning.
- **UI**: Provenance drawer on the Satellite context page shows provider, acquisition date, cloud cover, and the misuse warning. Source-status badges appear on status page and layer controls.

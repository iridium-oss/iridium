# Earth observation use cases in IRIDIUM

Sentinel-2 is wired into product use cases where it adds real value. Each use case is grounded in what Sentinel-2 can actually provide and exposes provenance and limitations.

## Corridor environmental context

- **What**: Vegetation (NDVI), water-sensitive (NDWI), and built-up (NDBI) along mobility corridors.
- **Use**: Planning and narrative context for green corridors, waterlogging risk, or urban footprint.
- **Provenance**: Scene acquisition date, cloud cover, provider, and index formula are shown.
- **Limitation**: Not realtime; not traffic or transit data.

## District-level green cover and built-up context

- **What**: District or AOI-level context for green space and impervious surface from NDVI and NDBI.
- **Use**: Mobility equity and resilience analysis; environmental context for district cards.
- **Provenance**: Same as above; intended interpretation is stated (e.g. vegetation context).
- **Limitation**: Derived indices; not calibrated to a specific regulatory metric without validation.

## Water and waterlogging context

- **What**: NDWI or water-sensitive index to indicate surface water or wetness.
- **Use**: Flood-sensitive or waterlogging context for route or district views.
- **Provenance**: Acquisition date and cloud cover; water presence is indicative, not flood mapping.
- **Limitation**: Not a flood forecast or realtime water level; use for context only.

## Mobility equity environmental overlays

- **What**: Green cover and built-up context overlays for equity dashboards.
- **Use**: Environmental context alongside mobility equity scores.
- **Provenance**: Source and acquisition time exposed; misuse warning that this is not transport telemetry.
- **Limitation**: Correlation with equity metrics requires separate analysis.

## Route context overlays

- **What**: Optional EO layer along a route or corridor in the map or route detail.
- **Use**: Visual and index context (NDVI/NDWI/NDBI) for the corridor.
- **Provenance**: Scene and layer provenance in drawer or panel.
- **Limitation**: Imagery is not realtime; use for planning and context.

## Urban growth and planning narratives

- **What**: Built-up and green indices over time (when multiple scenes are compared).
- **Use**: Urban expansion and construction pressure context for planning.
- **Provenance**: Per-scene acquisition and provider; comparison is not automated in the current implementation.
- **Limitation**: Multi-temporal analysis requires explicit scene selection and interpretation.

## What we do not do

- We do not use Sentinel-2 for fake live traffic, fake transit positions, or fake minute-level operational claims.
- We do not infer thermal surface temperature from Sentinel-2.
- We do not present indices as direct traffic or capacity truth.

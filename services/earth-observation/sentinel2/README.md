# Sentinel-2 integration

Sentinel-2 L2A imagery via STAC. Used as earth-observation context in IRIDIUM (urban footprint, green cover, water context). Not realtime traffic or transit.

## Providers

- **Primary**: Copernicus Data Space Ecosystem STAC
- **Fallback**: Earth Search STAC (Element 84)

## Indices

- NDVI (vegetation)
- NDWI (water-sensitive)
- NDBI (built-up)

Formulas and descriptors in `earth_observation/sentinel2/indices/formulas.py`.

## Area presets

Baku, Baku central district, corridor sample. See `manifests/areas.py`.

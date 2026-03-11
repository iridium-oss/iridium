# EO provenance

Earth observation layers in IRIDIUM expose full provenance. See [satellite-provenance.md](satellite-provenance.md) for the full model.

## Summary

- Every scene and layer includes: **source_provider**, **source_status**, **acquired_at**, **cloud_cover** (when available), **confidence_note**, **validation_note**.
- Index layers (NDVI, NDWI, NDBI) include formula and a **misuse_warning** that satellite context is not realtime traffic or transit data.
- API: `GET /api/v1/eo/provenance?scene_id=...` and layer endpoints return these fields.
- UI: Provenance drawer and source-status badges show provider, date, cloud cover, and the misuse warning.

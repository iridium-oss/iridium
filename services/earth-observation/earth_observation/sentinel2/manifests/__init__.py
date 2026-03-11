"""Area presets and manifests for EO search."""

from earth_observation.sentinel2.manifests.areas import (
    PRESETS,
    get_area_presets,
    get_bbox_for_preset,
)

__all__ = ["get_area_presets", "get_bbox_for_preset", "PRESETS"]

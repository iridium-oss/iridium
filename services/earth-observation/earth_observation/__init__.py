"""Earth observation service for IRIDIUM. Sentinel-2 and EO layer support."""

from earth_observation.sentinel2.search.search import search_scenes
from earth_observation.sentinel2.manifests.areas import get_area_presets, get_bbox_for_preset

__all__ = [
    "search_scenes",
    "get_area_presets",
    "get_bbox_for_preset",
]

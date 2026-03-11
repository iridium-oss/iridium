"""Sentinel-2 provider, search, and index layer support."""

from earth_observation.sentinel2.manifests.areas import get_area_presets, get_bbox_for_preset
from earth_observation.sentinel2.providers.base import Sentinel2ProviderProtocol
from earth_observation.sentinel2.search.search import search_scenes

__all__ = [
    "Sentinel2ProviderProtocol",
    "search_scenes",
    "get_area_presets",
    "get_bbox_for_preset",
]

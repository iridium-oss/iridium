"""Cache for EO search results and layer descriptors."""

from earth_observation.sentinel2.caching.cache import (
    get_cached_search,
    set_cached_search,
    get_cached_layer_descriptor,
    set_cached_layer_descriptor,
)

__all__ = [
    "get_cached_search",
    "set_cached_search",
    "get_cached_layer_descriptor",
    "set_cached_layer_descriptor",
]

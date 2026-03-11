"""Index and composite layer generation; AOI statistics."""

from earth_observation.sentinel2.processing.layers import (
    build_index_layer_descriptor,
    build_true_color_descriptor,
    get_overlay_descriptor,
)
from earth_observation.sentinel2.processing.stats import compute_aoi_stats_placeholder

__all__ = [
    "build_index_layer_descriptor",
    "build_true_color_descriptor",
    "get_overlay_descriptor",
    "compute_aoi_stats_placeholder",
]

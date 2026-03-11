"""
AOI statistics for EO layers. Placeholder for mean/min/max over area.
Full implementation would require raster read (e.g. rioxarray) and band math.
"""

from __future__ import annotations

from typing import Any

from iridium_schemas.earth_observation import EOScene


def compute_aoi_stats_placeholder(
    scene: EOScene,
    index_id: str,
    bbox: tuple[float, float, float, float],
) -> dict[str, Any]:
    """
    Placeholder for AOI summary statistics (mean, min, max) for an index over bbox.
    Real implementation would load scene assets, clip to bbox, compute index, then stats.
    Returns structure with status and note so API can expose it; values are null until implemented.
    """
    return {
        "scene_id": scene.scene_id,
        "index_id": index_id,
        "bbox": list(bbox),
        "status": "not_computed",
        "note": "AOI statistics require raster processing; use external GIS or Process API for values.",
        "mean": None,
        "min": None,
        "max": None,
        "pixel_count": None,
    }

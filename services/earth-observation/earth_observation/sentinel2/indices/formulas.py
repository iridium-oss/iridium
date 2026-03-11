"""
Defensible Sentinel-2 index formulas and metadata.
NDVI: vegetation. NDWI: water. NDBI: built-up.
All use standard band math; no thermal (Sentinel-2 does not provide thermal).
"""

from __future__ import annotations

from iridium_schemas.earth_observation import (
    EOIndexLayer,
    EOSceneMetadata,
)

MISUSE_WARNING = (
    "This layer is derived from satellite imagery. It is not realtime traffic, "
    "transit positions, or minute-level operational data. Use for environmental context only."
)

NDVI_FORMULA = "NDVI = (NIR - Red) / (NIR + Red). B08 (NIR), B04 (Red). Range typically -1 to 1; vegetation higher."
NDWI_FORMULA = (
    "NDWI = (Green - NIR) / (Green + NIR). B03 (Green), B08 (NIR). "
    "Water-sensitive; positive often indicates surface water."
)
NDBI_FORMULA = (
    "NDBI = (SWIR1 - NIR) / (SWIR1 + NIR). B11 (SWIR1), B08 (NIR). "
    "Built-up index; higher values often indicate impervious surfaces."
)


def get_index_descriptor(
    layer_id: str,
    scene_id: str | None,
    metadata: EOSceneMetadata,
    min_val: float | None = None,
    max_val: float | None = None,
) -> EOIndexLayer:
    """Build EOIndexLayer for a known index id (ndvi, ndwi, ndbi)."""
    if layer_id == "ndvi":
        return EOIndexLayer(
            layer_id="ndvi",
            name="NDVI (vegetation)",
            description="Normalized Difference Vegetation Index. Green vegetation context near corridors.",
            formula_note=NDVI_FORMULA,
            scene_id=scene_id,
            metadata=metadata,
            min_value=min_val or -1.0,
            max_value=max_val or 1.0,
            legend_units="dimensionless",
            misuse_warning=MISUSE_WARNING,
        )
    if layer_id == "ndwi":
        return EOIndexLayer(
            layer_id="ndwi",
            name="NDWI (water)",
            description="Normalized Difference Water Index. Surface water and waterlogging context.",
            formula_note=NDWI_FORMULA,
            scene_id=scene_id,
            metadata=metadata,
            min_value=min_val or -1.0,
            max_value=max_val or 1.0,
            legend_units="dimensionless",
            misuse_warning=MISUSE_WARNING,
        )
    if layer_id == "ndbi":
        return EOIndexLayer(
            layer_id="ndbi",
            name="NDBI (built-up)",
            description="Normalized Difference Built-up Index. Urban footprint and built-up context.",
            formula_note=NDBI_FORMULA,
            scene_id=scene_id,
            metadata=metadata,
            min_value=min_val or -1.0,
            max_value=max_val or 1.0,
            legend_units="dimensionless",
            misuse_warning=MISUSE_WARNING,
        )
    return EOIndexLayer(
        layer_id=layer_id,
        name=layer_id,
        description="Derived index layer.",
        scene_id=scene_id,
        metadata=metadata,
        min_value=min_val,
        max_value=max_val,
        misuse_warning=MISUSE_WARNING,
    )


def true_color_descriptor(scene_id: str | None, metadata: EOSceneMetadata) -> dict:
    """Descriptor for true-color composite (B04, B03, B02)."""
    return {
        "layer_id": "true-color",
        "name": "True color",
        "description": "Sentinel-2 true color composite (B04 Red, B03 Green, B02 Blue).",
        "scene_id": scene_id,
        "metadata": metadata,
        "type": "true_color",
        "misuse_warning": MISUSE_WARNING,
    }

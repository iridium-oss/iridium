"""
Build EO layer and overlay descriptors from a scene.
Deterministic; no raster I/O in this module (that would be in a separate pipeline).
"""

from __future__ import annotations

from typing import Any, Optional

from iridium_schemas.earth_observation import (
    EOScene,
    EOIndexLayer,
    EOTileLayer,
    EOOverlayDescriptor,
    EOSourceStatus,
)

from earth_observation.sentinel2.indices.formulas import get_index_descriptor, true_color_descriptor


def build_index_layer_descriptor(
    scene: EOScene,
    index_id: str,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
) -> EOIndexLayer:
    """Build index layer descriptor for ndvi, ndwi, or ndbi from scene metadata."""
    return get_index_descriptor(
        layer_id=index_id,
        scene_id=scene.scene_id,
        metadata=scene.metadata,
        min_val=min_val,
        max_val=max_val,
    )


def build_true_color_descriptor(scene: EOScene) -> dict[str, Any]:
    """Build true-color tile layer descriptor from scene."""
    return true_color_descriptor(scene.scene_id, scene.metadata)


def get_overlay_descriptor(
    scene: EOScene,
    layer_type: str,
    index_id: Optional[str] = None,
) -> EOOverlayDescriptor:
    """Build full overlay descriptor for UI. layer_type: index or tile; index_id for ndvi/ndwi/ndbi."""
    metadata = scene.metadata
    if layer_type == "tile":
        desc = build_true_color_descriptor(scene)
        tile_layer = EOTileLayer(
            layer_id="true-color",
            name=desc["name"],
            description=desc["description"],
            scene_id=scene.scene_id,
            metadata=metadata,
            type="true_color",
            tile_url_template=None,
            misuse_warning=desc.get("misuse_warning"),
        )
        return EOOverlayDescriptor(
            overlay_id=f"true-color-{scene.scene_id[:24]}",
            name=desc["name"],
            description=desc["description"],
            layer_type="tile",
            tile_layer=tile_layer,
            index_layer=None,
            source_provider=metadata.source_provider,
            source_status=metadata.source_status,
            acquired_at=metadata.acquired_at,
            cloud_cover=metadata.cloud_cover,
            intended_interpretation="True color composite for visual context.",
            misuse_warning=desc.get("misuse_warning"),
        )
    if layer_type == "index" and index_id:
        idx = build_index_layer_descriptor(scene, index_id)
        return EOOverlayDescriptor(
            overlay_id=f"{index_id}-{scene.scene_id[:24]}",
            name=idx.name,
            description=idx.description,
            layer_type="index",
            index_layer=idx,
            tile_layer=None,
            source_provider=metadata.source_provider,
            source_status=metadata.source_status,
            acquired_at=metadata.acquired_at,
            cloud_cover=metadata.cloud_cover,
            intended_interpretation=idx.formula_note or idx.description,
            misuse_warning=idx.misuse_warning,
        )
    return EOOverlayDescriptor(
        overlay_id="unknown",
        name="Unknown",
        description="Unknown layer",
        layer_type="index",
        source_provider=metadata.source_provider,
        source_status=EOSourceStatus.unavailable,
        acquired_at=metadata.acquired_at,
        cloud_cover=metadata.cloud_cover,
    )

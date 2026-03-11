"""
Area presets for EO search. Baku and corridor sample.
Bbox format: [minx, miny, maxx, maxy] (WGS84).
"""

from __future__ import annotations

from iridium_schemas.earth_observation import EOAreaPresetDefinition

# Baku approximate bounds (WGS84)
BAKU_BBOX = [49.72, 40.28, 50.05, 40.48]
# Central district smaller window
BAKU_CENTRAL_BBOX = [49.84, 40.36, 49.92, 40.42]
# Sample corridor (linear stretch)
CORRIDOR_SAMPLE_BBOX = [49.82, 40.38, 49.95, 40.42]

PRESETS: dict[str, EOAreaPresetDefinition] = {
    "baku": EOAreaPresetDefinition(
        preset_id="baku",
        name="Baku",
        bbox=BAKU_BBOX,
        description="Baku metropolitan area",
    ),
    "baku_district_central": EOAreaPresetDefinition(
        preset_id="baku_district_central",
        name="Baku central district",
        bbox=BAKU_CENTRAL_BBOX,
        description="Central district sample",
    ),
    "corridor_sample": EOAreaPresetDefinition(
        preset_id="corridor_sample",
        name="Corridor sample",
        bbox=CORRIDOR_SAMPLE_BBOX,
        description="Sample mobility corridor AOI",
    ),
}


def get_area_presets() -> list[EOAreaPresetDefinition]:
    """Return all defined area presets."""
    return list(PRESETS.values())


def get_bbox_for_preset(preset_id: str) -> tuple[float, float, float, float] | None:
    """Return (minx, miny, maxx, maxy) for a preset, or None if unknown."""
    p = PRESETS.get(preset_id)
    if not p or len(p.bbox) != 4:
        return None
    return (p.bbox[0], p.bbox[1], p.bbox[2], p.bbox[3])

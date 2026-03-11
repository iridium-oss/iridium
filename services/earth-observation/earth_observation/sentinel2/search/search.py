"""
Orchestrate Sentinel-2 scene search across providers.
Primary: Copernicus STAC. Fallback: Earth Search STAC.
"""

from __future__ import annotations

from datetime import datetime

from iridium_schemas.earth_observation import (
    EOSceneSearchResult,
    EOSourceStatus,
)

from earth_observation.sentinel2.manifests.areas import get_bbox_for_preset
from earth_observation.sentinel2.providers.copernicus_stac import CopernicusStacProvider
from earth_observation.sentinel2.providers.earth_search_stac import EarthSearchStacProvider


def search_scenes(
    bbox: tuple[float, float, float, float] | None = None,
    preset: str | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    cloud_cover_max: float | None = None,
    limit: int = 20,
    prefer_copernicus: bool = True,
) -> EOSceneSearchResult:
    """
    Search Sentinel-2 scenes. Provide either bbox or preset.
    Uses Copernicus first; on failure or empty, falls back to Earth Search.
    """
    if bbox is None and preset:
        bbox = get_bbox_for_preset(preset)
    if bbox is None:
        return EOSceneSearchResult(
            scenes=[],
            source_provider="none",
            source_status=EOSourceStatus.unavailable,
            note="No bbox or valid preset provided",
        )

    providers = []
    if prefer_copernicus:
        providers.append(CopernicusStacProvider())
        providers.append(EarthSearchStacProvider())
    else:
        providers.append(EarthSearchStacProvider())
        providers.append(CopernicusStacProvider())

    last_result: EOSceneSearchResult | None = None
    for prov in providers:
        if prov.status() == EOSourceStatus.unavailable:
            continue
        result = prov.search(
            bbox=bbox,
            date_start=date_start,
            date_end=date_end,
            cloud_cover_max=cloud_cover_max,
            limit=limit,
        )
        if result.scenes:
            return result
        last_result = result

    if last_result is not None:
        return last_result
    return EOSceneSearchResult(
        scenes=[],
        source_provider="none",
        source_status=EOSourceStatus.unavailable,
        bbox=list(bbox),
        date_start=date_start,
        date_end=date_end,
        cloud_cover_max=cloud_cover_max,
        note="No provider returned scenes",
    )

"""
Earth observation API. Sentinel-2 scene search, layers, provenance.
Not realtime traffic or transit. All responses include source status and acquisition metadata.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter()


class EOStatusResponse(BaseModel):
    enabled: bool
    data_status: str
    providers_available: list[str] = Field(default_factory=list)
    note: str | None = None


class EOProviderInfo(BaseModel):
    provider_id: str
    status: str
    note: str | None = None


class EOProvidersResponse(BaseModel):
    providers: list[EOProviderInfo] = Field(default_factory=list)
    note: str | None = None


class EOAreaResponse(BaseModel):
    areas: list[dict[str, Any]] = Field(default_factory=list)


class EOSceneSearchQuery(BaseModel):
    bbox: list[float] | None = None
    preset: str | None = None
    date_start: datetime | None = None
    date_end: datetime | None = None
    cloud_cover_max: float | None = Field(None, ge=0, le=100)
    limit: int = Field(20, ge=1, le=100)


class EOSceneResponse(BaseModel):
    scene_id: str
    collection: str
    metadata: dict[str, Any]
    assets: list[dict[str, Any]] = Field(default_factory=list)
    asset_links: dict[str, str] = Field(default_factory=dict)


class EOLayerResponse(BaseModel):
    layer_id: str
    name: str
    description: str
    scene_id: str | None = None
    source_provider: str
    source_status: str
    acquired_at: datetime | None = None
    cloud_cover: float | None = None
    formula_note: str | None = None
    misuse_warning: str | None = None
    legend_units: str | None = None
    min_value: float | None = None
    max_value: float | None = None


class EOProvenanceResponse(BaseModel):
    layer_id: str
    source_provider: str
    source_status: str
    acquired_at: datetime | None = None
    processed_at: datetime | None = None
    cloud_cover: float | None = None
    confidence_note: str | None = None
    validation_note: str | None = None
    misuse_warning: str | None = None


class EOStatsResponse(BaseModel):
    scene_id: str
    index_id: str
    bbox: list[float]
    status: str
    note: str | None = None
    mean: float | None = None
    min: float | None = None
    max: float | None = None


def _get_search():
    try:
        from earth_observation.sentinel2.search.search import search_scenes

        return search_scenes
    except ImportError:
        return None


def _get_area_presets():
    try:
        from earth_observation.sentinel2.manifests.areas import get_area_presets

        return get_area_presets
    except ImportError:
        return None


def _get_providers_status():
    try:
        from earth_observation.sentinel2.providers.copernicus_stac import CopernicusStacProvider
        from earth_observation.sentinel2.providers.earth_search_stac import EarthSearchStacProvider

        cop = CopernicusStacProvider()
        earth = EarthSearchStacProvider()
        return [
            ("copernicus_stac", cop.status()),
            ("earth_search_stac", earth.status()),
        ]
    except ImportError:
        return []


def _get_scene(scene_id: str):
    try:
        from earth_observation.sentinel2.providers.copernicus_stac import CopernicusStacProvider
        from earth_observation.sentinel2.providers.earth_search_stac import EarthSearchStacProvider

        for prov in [CopernicusStacProvider(), EarthSearchStacProvider()]:
            if prov.status().value != "unavailable":
                scene = prov.get_scene(scene_id)
                if scene:
                    return scene
    except ImportError:
        pass
    return None


def _build_layer_descriptor(scene_id: str, layer_type: str, index_id: str | None = None):
    try:
        from earth_observation.sentinel2.processing.layers import get_overlay_descriptor

        scene = _get_scene(scene_id)
        if not scene:
            return None
        return get_overlay_descriptor(scene, layer_type, index_id)
    except ImportError:
        return None


def _get_cached_search(bbox, preset, date_start, date_end, cloud_cover_max, limit):
    try:
        from earth_observation.sentinel2.caching.cache import get_cached_search, set_cached_search

        from app.core.settings import get_settings

        key = (bbox, preset, date_start, date_end, cloud_cover_max, limit)
        ttl = get_settings().eo.search_cache_ttl_seconds
        cached = get_cached_search(key, ttl=ttl)
        if cached is not None:
            return cached
        search_fn = _get_search()
        if not search_fn:
            return None
        bbox_t = tuple(bbox) if bbox and len(bbox) == 4 else None
        result = search_fn(
            bbox=bbox_t,
            preset=preset,
            date_start=date_start,
            date_end=date_end,
            cloud_cover_max=cloud_cover_max,
            limit=limit,
        )
        set_cached_search(key, result, ttl=ttl)
        return result
    except Exception:
        return None


@router.get(
    "/eo/status",
    response_model=EOStatusResponse,
    summary="Earth observation status",
    description="Reports whether EO (Sentinel-2) is enabled and which providers are available. Not realtime.",
)
def get_eo_status() -> EOStatusResponse:
    from app.core.settings import get_settings

    settings = get_settings()
    if not settings.eo.enabled:
        return EOStatusResponse(
            enabled=False,
            data_status="unavailable",
            note="Earth observation is disabled.",
        )
    providers = _get_providers_status()
    available = [p[0] for p in providers if p[1].value == "live"]
    return EOStatusResponse(
        enabled=True,
        data_status="live" if available else "unavailable",
        providers_available=available,
        note="Sentinel-2 is near-recent earth observation context, not realtime transport data.",
    )


@router.get(
    "/eo/providers",
    response_model=EOProvidersResponse,
    summary="EO providers status",
)
def get_eo_providers() -> EOProvidersResponse:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return EOProvidersResponse(note="EO disabled.")
    entries = _get_providers_status()
    return EOProvidersResponse(
        providers=[EOProviderInfo(provider_id=p[0], status=p[1].value, note=None) for p in entries],
    )


@router.get(
    "/eo/areas",
    response_model=EOAreaResponse,
    summary="EO area presets",
)
def get_eo_areas() -> EOAreaResponse:
    get_presets = _get_area_presets()
    if not get_presets:
        return EOAreaResponse(areas=[])
    presets = get_presets()
    return EOAreaResponse(
        areas=[p.model_dump() for p in presets],
    )


@router.get(
    "/eo/scenes/search",
    summary="Search Sentinel-2 scenes",
    description="Search by bbox or preset and optional date range and cloud cover. Returns scene metadata with provenance.",
)
def search_eo_scenes(
    bbox: str | None = Query(None, description="Comma-separated minx,miny,maxx,maxy"),
    preset: str | None = Query(None, description="Area preset id, e.g. baku"),
    date_start: datetime | None = Query(None),
    date_end: datetime | None = Query(None),
    cloud_cover_max: float | None = Query(None, ge=0, le=100),
    limit: int = Query(20, ge=1, le=100),
) -> dict[str, Any]:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return {
            "scenes": [],
            "source_provider": "none",
            "source_status": "unavailable",
            "note": "Earth observation is disabled.",
        }
    bbox_list = None
    if bbox:
        parts = [p.strip() for p in bbox.split(",")]
        if len(parts) == 4:
            try:
                bbox_list = [float(x) for x in parts]
            except ValueError:
                pass
    result = _get_cached_search(bbox_list, preset, date_start, date_end, cloud_cover_max, limit)
    if result is None:
        return {
            "scenes": [],
            "source_provider": "none",
            "source_status": "unavailable",
            "note": "Search not available; check EO service dependency.",
        }
    return {
        "scenes": [
            {
                "scene_id": s.scene_id,
                "collection": s.collection,
                "metadata": s.metadata.model_dump(mode="json"),
                "assets": [a.model_dump() for a in s.assets],
                "asset_links": s.asset_links,
            }
            for s in result.scenes
        ],
        "total_count": result.total_count,
        "source_provider": result.source_provider,
        "source_status": result.source_status.value,
        "searched_at": result.searched_at.isoformat() if result.searched_at else None,
        "bbox": result.bbox,
        "date_start": result.date_start.isoformat() if result.date_start else None,
        "date_end": result.date_end.isoformat() if result.date_end else None,
        "cloud_cover_max": result.cloud_cover_max,
        "note": result.note,
    }


@router.get(
    "/eo/scenes/{scene_id}",
    response_model=EOSceneResponse | None,
    summary="Get single EO scene",
)
def get_eo_scene(scene_id: str) -> dict[str, Any] | None:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return None
    scene = _get_scene(scene_id)
    if not scene:
        return None
    return {
        "scene_id": scene.scene_id,
        "collection": scene.collection,
        "metadata": scene.metadata.model_dump(mode="json"),
        "assets": [a.model_dump() for a in scene.assets],
        "asset_links": scene.asset_links,
    }


@router.get(
    "/eo/layers/true-color",
    summary="True color layer descriptor",
)
def get_eo_layer_true_color(
    scene_id: str = Query(..., description="Scene id from search"),
) -> dict[str, Any]:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return {"error": "EO disabled", "layer_id": "true-color"}
    desc = _build_layer_descriptor(scene_id, "tile")
    if not desc:
        return {"error": "Scene not found or layer unavailable", "scene_id": scene_id}
    return {
        "overlay_id": desc.overlay_id,
        "name": desc.name,
        "description": desc.description,
        "layer_type": desc.layer_type,
        "source_provider": desc.source_provider,
        "source_status": desc.source_status.value,
        "acquired_at": desc.acquired_at.isoformat() if desc.acquired_at else None,
        "cloud_cover": desc.cloud_cover,
        "intended_interpretation": desc.intended_interpretation,
        "misuse_warning": desc.misuse_warning,
    }


@router.get(
    "/eo/layers/ndvi",
    summary="NDVI layer descriptor",
)
def get_eo_layer_ndvi(
    scene_id: str = Query(..., description="Scene id from search"),
) -> dict[str, Any]:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return {"error": "EO disabled", "layer_id": "ndvi"}
    desc = _build_layer_descriptor(scene_id, "index", "ndvi")
    if not desc or not desc.index_layer:
        return {"error": "Scene not found or layer unavailable", "scene_id": scene_id}
    idx = desc.index_layer
    return {
        "layer_id": idx.layer_id,
        "name": idx.name,
        "description": idx.description,
        "formula_note": idx.formula_note,
        "scene_id": idx.scene_id,
        "source_provider": desc.source_provider,
        "source_status": desc.source_status.value,
        "acquired_at": desc.acquired_at.isoformat() if desc.acquired_at else None,
        "cloud_cover": desc.cloud_cover,
        "min_value": idx.min_value,
        "max_value": idx.max_value,
        "legend_units": idx.legend_units,
        "misuse_warning": idx.misuse_warning,
    }


@router.get(
    "/eo/layers/ndwi",
    summary="NDWI layer descriptor",
)
def get_eo_layer_ndwi(
    scene_id: str = Query(..., description="Scene id from search"),
) -> dict[str, Any]:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return {"error": "EO disabled", "layer_id": "ndwi"}
    desc = _build_layer_descriptor(scene_id, "index", "ndwi")
    if not desc or not desc.index_layer:
        return {"error": "Scene not found or layer unavailable", "scene_id": scene_id}
    idx = desc.index_layer
    return {
        "layer_id": idx.layer_id,
        "name": idx.name,
        "description": idx.description,
        "formula_note": idx.formula_note,
        "scene_id": idx.scene_id,
        "source_provider": desc.source_provider,
        "source_status": desc.source_status.value,
        "acquired_at": desc.acquired_at.isoformat() if desc.acquired_at else None,
        "cloud_cover": desc.cloud_cover,
        "min_value": idx.min_value,
        "max_value": idx.max_value,
        "legend_units": idx.legend_units,
        "misuse_warning": idx.misuse_warning,
    }


@router.get(
    "/eo/layers/ndbi",
    summary="NDBI layer descriptor",
)
def get_eo_layer_ndbi(
    scene_id: str = Query(..., description="Scene id from search"),
) -> dict[str, Any]:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return {"error": "EO disabled", "layer_id": "ndbi"}
    desc = _build_layer_descriptor(scene_id, "index", "ndbi")
    if not desc or not desc.index_layer:
        return {"error": "Scene not found or layer unavailable", "scene_id": scene_id}
    idx = desc.index_layer
    return {
        "layer_id": idx.layer_id,
        "name": idx.name,
        "description": idx.description,
        "formula_note": idx.formula_note,
        "scene_id": idx.scene_id,
        "source_provider": desc.source_provider,
        "source_status": desc.source_status.value,
        "acquired_at": desc.acquired_at.isoformat() if desc.acquired_at else None,
        "cloud_cover": desc.cloud_cover,
        "min_value": idx.min_value,
        "max_value": idx.max_value,
        "legend_units": idx.legend_units,
        "misuse_warning": idx.misuse_warning,
    }


@router.get(
    "/eo/stats",
    summary="AOI statistics (placeholder)",
)
def get_eo_stats(
    scene_id: str = Query(...),
    index_id: str = Query(..., description="ndvi, ndwi, or ndbi"),
    bbox: str = Query(..., description="minx,miny,maxx,maxy"),
) -> dict[str, Any]:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return {"status": "unavailable", "note": "EO disabled."}
    try:
        from earth_observation.sentinel2.processing.stats import compute_aoi_stats_placeholder

        scene = _get_scene(scene_id)
        if not scene:
            return {"status": "unavailable", "note": "Scene not found.", "scene_id": scene_id}
        parts = [p.strip() for p in bbox.split(",")]
        if len(parts) != 4:
            return {"status": "invalid", "note": "bbox must be minx,miny,maxx,maxy"}
        bbox_t = (float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]))
        out = compute_aoi_stats_placeholder(scene, index_id, bbox_t)
        return {k: v for k, v in out.items()}
    except ImportError:
        return {"status": "unavailable", "note": "EO processing not available."}


@router.get(
    "/eo/provenance",
    summary="Provenance for a scene or layer",
)
def get_eo_provenance(
    scene_id: str = Query(...),
    layer_id: str | None = Query(None, description="Optional: true-color, ndvi, ndwi, ndbi"),
) -> dict[str, Any]:
    from app.core.settings import get_settings

    if not get_settings().eo.enabled:
        return {"source_provider": "none", "source_status": "unavailable", "note": "EO disabled."}
    scene = _get_scene(scene_id)
    if not scene:
        return {
            "source_provider": "unknown",
            "source_status": "unavailable",
            "note": "Scene not found.",
        }
    m = scene.metadata
    return {
        "scene_id": scene_id,
        "source_provider": m.source_provider,
        "source_family": m.source_family,
        "source_status": m.source_status.value,
        "acquired_at": m.acquired_at.isoformat() if m.acquired_at else None,
        "processed_at": m.processed_at.isoformat() if m.processed_at else None,
        "cloud_cover": m.cloud_cover,
        "confidence_note": m.confidence_note,
        "validation_note": m.validation_note,
        "layer_id": layer_id,
        "misuse_warning": "Satellite context is not realtime traffic or transit data. Use for environmental context only.",
    }

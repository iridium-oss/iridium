"""
Earth observation schema contracts for IRIDIUM.

Shared models for Sentinel-2 and other EO sources. Every record includes
source_provider, source_family, source_status, acquired_at, cloud_cover when available,
and validation/confidence notes. Do not use for realtime traffic or transit positions.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class EOSourceStatus(str, Enum):
    """Status of the EO data source or layer."""

    live = "live"
    cached = "cached"
    unavailable = "unavailable"
    configuration_required = "configuration_required"
    permission_required = "permission_required"
    stale = "stale"


class EOAreaPreset(str, Enum):
    """Named area presets for EO search."""

    baku = "baku"
    baku_district_central = "baku_district_central"
    corridor_sample = "corridor_sample"


class EOBandAsset(BaseModel):
    """Single band or asset reference (e.g. B04, B08)."""

    band_name: str = Field(..., description="Band identifier, e.g. B04, B08")
    asset_key: Optional[str] = Field(None, description="STAC asset key if different")
    resolution_m: Optional[int] = Field(None, description="Spatial resolution in metres")
    href: Optional[str] = Field(None, description="Direct link when available")


class EOSceneMetadata(BaseModel):
    """Core metadata for an EO scene with provenance."""

    source_provider: str = Field(..., description="Provider id, e.g. copernicus_stac, earth_search")
    source_family: str = Field(default="stac_catalog", description="Source family")
    source_status: EOSourceStatus = Field(..., description="Availability status")
    acquired_at: Optional[datetime] = Field(None, description="Scene acquisition datetime (UTC)")
    processed_at: Optional[datetime] = Field(None, description="Processing time if derived")
    cloud_cover: Optional[float] = Field(None, ge=0, le=100, description="Cloud cover percentage")
    bbox: Optional[list[float]] = Field(None, description="Bounding box [minx, miny, maxx, maxy]")
    geometry: Optional[dict[str, Any]] = Field(None, description="GeoJSON geometry when available")
    confidence_note: Optional[str] = Field(None, description="Confidence or interpretation note")
    validation_note: Optional[str] = Field(None, description="Validation or quality note")


class EOScene(BaseModel):
    """Single EO scene (e.g. one Sentinel-2 granule)."""

    scene_id: str = Field(..., description="Unique scene identifier")
    collection: str = Field(..., description="STAC collection id")
    metadata: EOSceneMetadata
    assets: list[EOBandAsset] = Field(default_factory=list)
    asset_links: dict[str, str] = Field(default_factory=dict, description="Asset key to href mapping")


class EOSceneSearchResult(BaseModel):
    """Result of an EO scene search with provenance."""

    scenes: list[EOScene] = Field(default_factory=list)
    total_count: Optional[int] = None
    source_provider: str
    source_status: EOSourceStatus
    searched_at: Optional[datetime] = None
    bbox: Optional[list[float]] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    cloud_cover_max: Optional[float] = None
    note: Optional[str] = None


class EOIndexLayer(BaseModel):
    """Descriptor for a derived index layer (NDVI, NDWI, NDBI)."""

    layer_id: str = Field(..., description="Layer identifier, e.g. ndvi, ndwi, ndbi")
    name: str
    description: str = Field(..., description="Human-readable description and formula")
    formula_note: Optional[str] = Field(None, description="Formula or interpretation")
    scene_id: Optional[str] = None
    metadata: EOSceneMetadata
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    legend_units: Optional[str] = None
    misuse_warning: Optional[str] = Field(
        None,
        description="Warning that this is not traffic or realtime data",
    )


class EOTileLayer(BaseModel):
    """Descriptor for a tile or imagery layer (e.g. true-color composite)."""

    layer_id: str
    name: str
    description: str
    scene_id: Optional[str] = None
    metadata: EOSceneMetadata
    type: str = Field(..., description="e.g. true_color, false_color")
    tile_url_template: Optional[str] = None
    misuse_warning: Optional[str] = None


class EOOverlayDescriptor(BaseModel):
    """Descriptor for an EO overlay shown in the UI."""

    overlay_id: str
    name: str
    description: str
    layer_type: str = Field(..., description="index or tile")
    index_layer: Optional[EOIndexLayer] = None
    tile_layer: Optional[EOTileLayer] = None
    source_provider: str
    source_status: EOSourceStatus
    acquired_at: Optional[datetime] = None
    cloud_cover: Optional[float] = None
    intended_interpretation: Optional[str] = None
    misuse_warning: Optional[str] = None


class EOProcessingJob(BaseModel):
    """Reference to an EO processing job (async index generation)."""

    job_id: str
    status: str = Field(..., description="pending, running, completed, failed")
    scene_id: Optional[str] = None
    layer_id: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    note: Optional[str] = None


class EOAreaPresetDefinition(BaseModel):
    """Definition of a named area for EO search."""

    preset_id: str
    name: str
    bbox: list[float] = Field(..., min_length=4, max_length=4)
    description: Optional[str] = None

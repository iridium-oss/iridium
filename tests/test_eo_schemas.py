"""Tests for earth observation schemas."""

from datetime import datetime, timezone

import pytest

from iridium_schemas.earth_observation import (
    EOSourceStatus,
    EOAreaPreset,
    EOBandAsset,
    EOSceneMetadata,
    EOScene,
    EOSceneSearchResult,
    EOIndexLayer,
    EOTileLayer,
    EOOverlayDescriptor,
    EOAreaPresetDefinition,
)


def test_eo_source_status_values():
    assert EOSourceStatus.live.value == "live"
    assert EOSourceStatus.unavailable.value == "unavailable"
    assert EOSourceStatus.cached.value == "cached"


def test_eo_band_asset():
    a = EOBandAsset(band_name="B04", asset_key="B04", resolution_m=10, href="https://example.com/b04.tif")
    assert a.band_name == "B04"
    assert a.resolution_m == 10


def test_eo_scene_metadata():
    m = EOSceneMetadata(
        source_provider="earth_search_stac",
        source_family="stac_catalog",
        source_status=EOSourceStatus.live,
        acquired_at=datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc),
        cloud_cover=10.5,
        bbox=[49.8, 40.3, 49.9, 40.4],
        confidence_note="Test",
    )
    assert m.source_provider == "earth_search_stac"
    assert m.cloud_cover == 10.5
    assert m.bbox == [49.8, 40.3, 49.9, 40.4]


def test_eo_scene_metadata_cloud_cover_bounds():
    with pytest.raises(ValueError):
        EOSceneMetadata(
            source_provider="x",
            source_status=EOSourceStatus.live,
            cloud_cover=150,
        )


def test_eo_scene():
    m = EOSceneMetadata(
        source_provider="test",
        source_status=EOSourceStatus.live,
    )
    s = EOScene(
        scene_id="S2A_xxx",
        collection="sentinel-2-l2a",
        metadata=m,
        assets=[EOBandAsset(band_name="B04")],
        asset_links={"B04": "https://example.com/b04.tif"},
    )
    assert s.scene_id == "S2A_xxx"
    assert len(s.assets) == 1
    assert s.asset_links["B04"] == "https://example.com/b04.tif"


def test_eo_scene_search_result():
    r = EOSceneSearchResult(
        scenes=[],
        source_provider="earth_search_stac",
        source_status=EOSourceStatus.live,
        total_count=0,
        bbox=[49.8, 40.3, 49.9, 40.4],
    )
    assert r.source_provider == "earth_search_stac"
    assert r.total_count == 0


def test_eo_index_layer():
    m = EOSceneMetadata(source_provider="test", source_status=EOSourceStatus.live)
    layer = EOIndexLayer(
        layer_id="ndvi",
        name="NDVI",
        description="Vegetation index",
        formula_note="(NIR-Red)/(NIR+Red)",
        metadata=m,
        min_value=-1.0,
        max_value=1.0,
        legend_units="dimensionless",
        misuse_warning="Not realtime.",
    )
    assert layer.layer_id == "ndvi"
    assert layer.min_value == -1.0
    assert layer.misuse_warning == "Not realtime."


def test_eo_area_preset_definition():
    p = EOAreaPresetDefinition(
        preset_id="baku",
        name="Baku",
        bbox=[49.72, 40.28, 50.05, 40.48],
        description="Baku area",
    )
    assert p.preset_id == "baku"
    assert len(p.bbox) == 4

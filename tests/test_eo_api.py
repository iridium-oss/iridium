"""Tests for Earth Observation API endpoints."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "packages" / "schemas"))
sys.path.insert(0, str(root / "apps" / "api"))

from app.main import app
from iridium_schemas.earth_observation import (
    EOSceneSearchResult,
    EOScene,
    EOSceneMetadata,
    EOSourceStatus,
    EOBandAsset,
)

client = TestClient(app)


def _make_scene(scene_id: str = "S2A_Test_001") -> EOScene:
    return EOScene(
        scene_id=scene_id,
        collection="sentinel-2-l2a",
        metadata=EOSceneMetadata(
            source_provider="earth_search_stac",
            source_family="stac_catalog",
            source_status=EOSourceStatus.live,
            acquired_at=datetime(2024, 6, 1, 10, 0, tzinfo=timezone.utc),
            cloud_cover=15.0,
            bbox=[49.8, 40.3, 49.95, 40.45],
        ),
        assets=[EOBandAsset(band_name="B04"), EOBandAsset(band_name="B08")],
        asset_links={"B04": "https://example.com/B04.tif", "B08": "https://example.com/B08.tif"},
    )


def test_eo_status():
    response = client.get("/api/v1/eo/status")
    assert response.status_code == 200
    data = response.json()
    assert "enabled" in data
    assert "data_status" in data
    assert "providers_available" in data


def test_eo_providers():
    response = client.get("/api/v1/eo/providers")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data


def test_eo_areas():
    response = client.get("/api/v1/eo/areas")
    assert response.status_code == 200
    data = response.json()
    assert "areas" in data


def test_eo_scenes_search_no_params():
    response = client.get("/api/v1/eo/scenes/search")
    assert response.status_code == 200
    data = response.json()
    assert "scenes" in data
    assert "source_status" in data


def test_eo_scenes_search_with_preset():
    with patch("app.api.eo._get_cached_search") as mock:
        mock.return_value = EOSceneSearchResult(
            scenes=[_make_scene()],
            total_count=1,
            source_provider="earth_search_stac",
            source_status=EOSourceStatus.live,
            searched_at=datetime.now(timezone.utc),
            bbox=[49.72, 40.28, 50.05, 40.48],
        )
        response = client.get("/api/v1/eo/scenes/search?preset=baku&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["scenes"]) == 1
        assert data["scenes"][0]["scene_id"] == "S2A_Test_001"
        assert data["source_provider"] == "earth_search_stac"


def test_eo_provenance():
    with patch("app.api.eo._get_scene") as mock:
        mock.return_value = _make_scene("S2A_Provenance_001")
        response = client.get("/api/v1/eo/provenance?scene_id=S2A_Provenance_001")
        assert response.status_code == 200
        data = response.json()
        assert data["scene_id"] == "S2A_Provenance_001"
        assert data["source_provider"] == "earth_search_stac"
        assert "misuse_warning" in data


def test_eo_provenance_scene_not_found():
    with patch("app.api.eo._get_scene") as mock:
        mock.return_value = None
        response = client.get("/api/v1/eo/provenance?scene_id=NonExistent")
        assert response.status_code == 200
        data = response.json()
        assert data["source_status"] == "unavailable"


def test_eo_layer_ndvi():
    with patch("app.api.eo._build_layer_descriptor") as mock:
        from iridium_schemas.earth_observation import EOOverlayDescriptor, EOIndexLayer
        desc = MagicMock(spec=EOOverlayDescriptor)
        desc.index_layer = EOIndexLayer(
            layer_id="ndvi",
            name="NDVI (vegetation)",
            description="Vegetation index",
            metadata=EOSceneMetadata(source_provider="test", source_status=EOSourceStatus.live),
            min_value=-1.0,
            max_value=1.0,
            misuse_warning="Not realtime.",
        )
        desc.source_provider = "earth_search_stac"
        desc.source_status = EOSourceStatus.live
        desc.acquired_at = datetime(2024, 6, 1, tzinfo=timezone.utc)
        desc.cloud_cover = 10.0
        mock.return_value = desc
        response = client.get("/api/v1/eo/layers/ndvi?scene_id=S2A_Test")
        assert response.status_code == 200
        data = response.json()
        assert data["layer_id"] == "ndvi"
        assert data["misuse_warning"] == "Not realtime."


def test_eo_layer_ndvi_scene_not_found():
    with patch("app.api.eo._build_layer_descriptor") as mock:
        mock.return_value = None
        response = client.get("/api/v1/eo/layers/ndvi?scene_id=BadId")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data


def test_eo_stats():
    response = client.get(
        "/api/v1/eo/stats?scene_id=S2A_Test&index_id=ndvi&bbox=49.8,40.3,49.9,40.4"
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "scene_id" in data or "note" in data

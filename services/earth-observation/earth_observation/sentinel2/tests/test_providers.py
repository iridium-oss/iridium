"""Tests for STAC provider parsing and normalization."""

from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

import pytest

from earth_observation.sentinel2.providers.earth_search_stac import (
    EarthSearchStacProvider,
    _scene_from_feature,
)
from iridium_schemas.earth_observation import EOSourceStatus


def test_scene_from_feature_minimal():
    feature = {
        "id": "S2A_MSIL2A_20240115T100001",
        "properties": {
            "datetime": "2024-01-15T10:00:01Z",
            "eo:cloud_cover": 12.5,
            "collection": "sentinel-2-l2a",
        },
        "bbox": [49.8, 40.3, 49.9, 40.4],
        "geometry": {"type": "Polygon", "coordinates": [[]]},
        "assets": {
            "B04": {"href": "https://example.com/B04.tif"},
            "B08": {"href": "https://example.com/B08.tif"},
        },
    }
    scene = _scene_from_feature(feature, "earth_search_stac")
    assert scene.scene_id == "S2A_MSIL2A_20240115T100001"
    assert scene.collection == "sentinel-2-l2a"
    assert scene.metadata.source_provider == "earth_search_stac"
    assert scene.metadata.cloud_cover == 12.5
    assert scene.metadata.bbox == [49.8, 40.3, 49.9, 40.4]
    assert "B04" in scene.asset_links
    assert scene.asset_links["B04"] == "https://example.com/B04.tif"


def test_scene_from_feature_no_cloud():
    feature = {
        "id": "S2B_Test",
        "properties": {"collection": "sentinel-2-l2a"},
        "assets": {},
    }
    scene = _scene_from_feature(feature, "earth_search_stac")
    assert scene.metadata.cloud_cover is None


@patch("earth_observation.sentinel2.providers.earth_search_stac.httpx.Client")
def test_earth_search_search(mock_client_class):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {
        "features": [
            {
                "id": "S2A_Item_1",
                "properties": {"datetime": "2024-06-01T10:00:00Z", "eo:cloud_cover": 5, "collection": "sentinel-2-l2a"},
                "bbox": [49.8, 40.3, 49.9, 40.4],
                "geometry": None,
                "assets": {"B04": {"href": "https://x.com/B04.tif"}},
            }
        ],
        "numberMatched": 1,
    }
    mock_client = MagicMock()
    mock_client.__enter__.return_value.post.return_value = mock_resp
    mock_client_class.return_value = mock_client

    prov = EarthSearchStacProvider()
    result = prov.search(bbox=(49.8, 40.3, 49.9, 40.4), limit=5)
    assert result.source_provider == "earth_search_stac"
    assert result.source_status == EOSourceStatus.live
    assert len(result.scenes) == 1
    assert result.scenes[0].scene_id == "S2A_Item_1"

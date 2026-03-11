"""Tests for index formulas and layer descriptors."""

from iridium_schemas.earth_observation import (
    EOSceneMetadata,
    EOSourceStatus,
)

from earth_observation.sentinel2.indices.formulas import (
    get_index_descriptor,
    NDVI_FORMULA,
    NDWI_FORMULA,
    NDBI_FORMULA,
    MISUSE_WARNING,
)


def test_ndvi_formula_contains_bands():
    assert "B08" in NDVI_FORMULA or "NIR" in NDVI_FORMULA
    assert "Red" in NDVI_FORMULA or "B04" in NDVI_FORMULA


def test_ndwi_formula_contains_bands():
    assert "Green" in NDWI_FORMULA or "B03" in NDWI_FORMULA
    assert "NIR" in NDWI_FORMULA or "B08" in NDWI_FORMULA


def test_ndbi_formula_contains_bands():
    assert "SWIR" in NDBI_FORMULA or "B11" in NDBI_FORMULA


def test_misuse_warning_not_realtime():
    assert "realtime" in MISUSE_WARNING.lower() or "traffic" in MISUSE_WARNING.lower()


def test_get_index_descriptor_ndvi():
    m = EOSceneMetadata(source_provider="test", source_status=EOSourceStatus.live)
    layer = get_index_descriptor("ndvi", "S2A_001", m, -0.5, 0.9)
    assert layer.layer_id == "ndvi"
    assert layer.name == "NDVI (vegetation)"
    assert layer.misuse_warning == MISUSE_WARNING
    assert layer.min_value == -0.5
    assert layer.max_value == 0.9


def test_get_index_descriptor_ndwi():
    m = EOSceneMetadata(source_provider="test", source_status=EOSourceStatus.live)
    layer = get_index_descriptor("ndwi", "S2A_002", m)
    assert layer.layer_id == "ndwi"
    assert layer.min_value == -1.0
    assert layer.max_value == 1.0


def test_get_index_descriptor_ndbi():
    m = EOSceneMetadata(source_provider="test", source_status=EOSourceStatus.live)
    layer = get_index_descriptor("ndbi", None, m)
    assert layer.layer_id == "ndbi"

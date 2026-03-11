"""Tests for area presets and bbox resolution."""

from earth_observation.sentinel2.manifests.areas import (
    PRESETS,
    get_area_presets,
    get_bbox_for_preset,
)


def test_get_area_presets():
    presets = get_area_presets()
    assert len(presets) >= 1
    ids = [p.preset_id for p in presets]
    assert "baku" in ids


def test_get_bbox_for_preset_baku():
    bbox = get_bbox_for_preset("baku")
    assert bbox is not None
    assert len(bbox) == 4
    assert bbox[0] < bbox[2]
    assert bbox[1] < bbox[3]


def test_get_bbox_for_preset_unknown():
    assert get_bbox_for_preset("unknown_preset") is None


def test_presets_have_bbox():
    for p in PRESETS.values():
        assert len(p.bbox) == 4
        assert p.bbox[0] < p.bbox[2]
        assert p.bbox[1] < p.bbox[3]

"""Ingestion pipeline tests."""

import json
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "packages" / "schemas"))
sys.path.insert(0, str(root / "services" / "ingestion"))

from ingestion.pipeline import _load_json_or_csv, run_ingestion, validate_batch
from iridium_schemas.events import GNSSPoint, IngestionEventBatch, SensorEvent


def test_validate_batch_ok():
    batch = IngestionEventBatch(
        sensor_events=[
            SensorEvent(segment_id="e1", timestamp=datetime.now(UTC), speed_kmh=30.0)
        ]
    )
    ok, errors = validate_batch(batch)
    assert ok is True
    assert len(errors) == 0


def test_validate_batch_invalid_speed():
    # Use model_construct so invalid speed_kmh (300) bypasses Pydantic validation;
    # validate_batch() then catches it via its own range check.
    invalid_ev = SensorEvent.model_construct(
        segment_id="e1", timestamp=datetime.now(UTC), speed_kmh=300
    )
    batch = IngestionEventBatch.model_construct(sensor_events=[invalid_ev])
    ok, errors = validate_batch(batch)
    assert ok is False
    assert len(errors) >= 1


def test_run_ingestion_synthetic():
    data_root = root / "data"
    samples = data_root / "samples"
    synthetic = data_root / "synthetic"
    count, errs = run_ingestion(samples, synthetic)
    assert count >= 0
    assert isinstance(errs, list)


def test_validate_batch_gnss_missing_segment_or_lat():
    """Cover validate_batch gnss_points branch (segment_id None and lat None)."""
    bad_gnss = GNSSPoint.model_construct(
        segment_id=None, lat=None, lon=49.0, timestamp=datetime.now(UTC)
    )
    batch = IngestionEventBatch.model_construct(sensor_events=[], gnss_points=[bad_gnss])
    ok, errors = validate_batch(batch)
    assert ok is False
    assert any("gnss_points" in e for e in errors)


def test_load_json_or_csv_missing_path():
    """Cover _load_json_or_csv when path does not exist."""
    out = _load_json_or_csv(Path("/nonexistent/file.json"))
    assert out == []


def test_load_json_or_csv_unknown_extension_returns_empty():
    """Cover _load_json_or_csv final return [] for non-.json/.csv."""
    path = Path(tempfile.gettempdir()) / f"test_ingestion_{id(object())}.txt"
    try:
        path.write_text("hello", encoding="utf-8")
        out = _load_json_or_csv(path)
        assert out == []
    finally:
        path.unlink(missing_ok=True)


def test_load_json_or_csv_csv_file():
    """Cover _load_json_or_csv .csv branch."""
    path = Path(tempfile.gettempdir()) / f"test_ingestion_{id(object())}.csv"
    try:
        path.write_text("a,b\n1,2\n", encoding="utf-8")
        out = _load_json_or_csv(path)
        assert out == [{"a": "1", "b": "2"}]
    finally:
        path.unlink(missing_ok=True)


def test_run_ingestion_weather_and_public_events():
    """Cover run_ingestion branches for WeatherSnapshot and PublicEventRecord."""
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        (base / "weather.json").write_text(
            json.dumps(
                [{"region_id": "baku", "timestamp": "2025-03-08T10:00:00Z", "temp_c": 12.0}]
            ),
            encoding="utf-8",
        )
        (base / "events.json").write_text(
            json.dumps(
                [
                    {
                        "event_id": "ev1",
                        "start_time": "2025-03-08T14:00:00Z",
                        "end_time": "2025-03-08T17:00:00Z",
                        "venue_or_zone_id": "z1",
                        "capacity": 100,
                        "event_type": "other",
                    }
                ]
            ),
            encoding="utf-8",
        )
        count, errs = run_ingestion(base, Path("/nonexistent"))
        assert count >= 1
        assert isinstance(errs, list)

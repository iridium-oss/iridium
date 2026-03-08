"""Ingestion pipeline tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "packages" / "schemas"))
sys.path.insert(0, str(root / "services" / "ingestion"))

from iridium_schemas.events import IngestionEventBatch, SensorEvent
from datetime import datetime
from ingestion.pipeline import validate_batch, run_ingestion


def test_validate_batch_ok():
    batch = IngestionEventBatch(
        sensor_events=[SensorEvent(segment_id="e1", timestamp=datetime.utcnow(), speed_kmh=30.0)]
    )
    ok, errors = validate_batch(batch)
    assert ok is True
    assert len(errors) == 0


def test_validate_batch_invalid_speed():
    # Use model_construct so invalid speed_kmh (300) bypasses Pydantic validation;
    # validate_batch() then catches it via its own range check.
    invalid_ev = SensorEvent.model_construct(
        segment_id="e1", timestamp=datetime.utcnow(), speed_kmh=300
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

"""
Baseline ingestion pipeline. Reads sample files, validates, and stages in memory.
Future: Kafka/Redis streams, persistence to digital twin store.
"""

from pathlib import Path
from typing import Any

from iridium_schemas.events import (
    SensorEvent,
    GNSSPoint,
    WeatherSnapshot,
    PublicEventRecord,
    IngestionEventBatch,
)
from pydantic import ValidationError


def validate_batch(batch: IngestionEventBatch) -> tuple[bool, list[str]]:
    """Validate a batch; return (ok, list of error messages)."""
    errors: list[str] = []
    for i, e in enumerate(batch.sensor_events):
        if e.speed_kmh is not None and (e.speed_kmh < 0 or e.speed_kmh > 200):
            errors.append(f"sensor_events[{i}].speed_kmh out of range")
    for i, e in enumerate(batch.gnss_points):
        if e.segment_id is None and e.lat is None:
            errors.append(f"gnss_points[{i}] missing segment_id or lat/lon")
    return len(errors) == 0, errors


def _load_json_or_csv(path: Path) -> list[dict[str, Any]]:
    """Load JSON array or CSV into list of dicts. Placeholder: return empty if file missing."""
    if not path.exists():
        return []
    import json
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    if path.suffix.lower() == ".csv":
        import csv
        from io import StringIO
        rows = list(csv.DictReader(StringIO(text)))
        return rows
    return []


def run_ingestion(
    samples_dir: Path,
    synthetic_dir: Path,
) -> tuple[int, list[str]]:
    """
    Run ingestion from data/samples and data/synthetic. Returns (count of records staged, errors).
    Baseline: parse files, validate, return count. No persistence yet.
    """
    errors: list[str] = []
    count = 0
    for dir_path in (samples_dir, synthetic_dir):
        if not dir_path.exists():
            continue
        for path in dir_path.rglob("*.json"):
            for row in _load_json_or_csv(path):
                try:
                    if "segment_id" in row and "timestamp" in row:
                        SensorEvent.model_validate(row)
                        count += 1
                    elif "lat" in row and "lon" in row and "timestamp" in row:
                        GNSSPoint.model_validate(row)
                        count += 1
                    elif "region_id" in row and "timestamp" in row:
                        WeatherSnapshot.model_validate(row)
                        count += 1
                    elif "event_id" in row and "start_time" in row:
                        PublicEventRecord.model_validate(row)
                        count += 1
                except (ValidationError, TypeError) as e:
                    errors.append(f"{path.name}: {str(e)}")
    return count, errors

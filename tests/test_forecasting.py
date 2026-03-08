"""Forecasting baseline tests."""

import sys
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/digital-twin", "services/forecasting"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from forecasting.pipeline import get_congestion_forecast


def test_congestion_forecast_default():
    result = get_congestion_forecast(horizon_minutes=60)
    assert result.horizon_minutes == 60
    assert len(result.segments) >= 1
    assert result.model_version == "baseline-heuristic"


def test_congestion_forecast_with_segments():
    result = get_congestion_forecast(horizon_minutes=30, segment_ids=["e1", "e2"])
    assert result.horizon_minutes == 30
    assert all(s.segment_id in ("e1", "e2") for s in result.segments)


def test_forecast_segment_fields():
    result = get_congestion_forecast(horizon_minutes=15)
    s = result.segments[0]
    assert s.timestamp is not None
    assert s.congestion_score is None or 0 <= s.congestion_score <= 1

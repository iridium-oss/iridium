"""Forecasting baseline tests."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/digital-twin", "services/forecasting"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from forecasting.pipeline import get_congestion_forecast
from iridium_schemas.network import NetworkEdge


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


def test_congestion_forecast_with_twin_edges():
    """Cover _baseline_congestion loop when snapshot has edges with edge_id, speed_kmh, occupancy_pct."""
    edges = [
        NetworkEdge(
            edge_id="e1",
            from_node="n1",
            to_node="n2",
            mode="road",
            speed_kmh=25.0,
            occupancy_pct=30.0,
        ),
        NetworkEdge(edge_id="e2", from_node="n2", to_node="n3", mode="road"),
    ]
    snap = MagicMock()
    snap.edges = edges
    snap.data_status = "live"
    with patch("forecasting.pipeline.get_assembled_snapshot", return_value=snap):
        result = get_congestion_forecast(horizon_minutes=30, segment_ids=["e1"])
    assert len(result.segments) >= 1
    assert any(s.segment_id == "e1" for s in result.segments)


def test_congestion_forecast_metadata():
    """Production baseline must expose model_type, model_maturity, confidence_note, no fallback."""
    result = get_congestion_forecast(horizon_minutes=60)
    assert result.model_type == "deterministic_baseline"
    assert result.model_maturity == "production_baseline"
    assert result.fallback_used is False
    assert result.confidence_note is not None
    assert "baseline" in (result.confidence_note or "").lower()

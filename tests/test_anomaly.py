"""Anomaly detection tests."""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/digital-twin", "services/anomaly-detection"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from anomaly_detection.detector import get_anomalies
from iridium_schemas.network import DigitalTwinSnapshot, NetworkEdge


def test_get_anomalies_returns_list():
    result = get_anomalies()
    assert isinstance(result, list)


def test_get_anomalies_since_filter():
    since = datetime.now(UTC) - timedelta(hours=1)
    result = get_anomalies(since=since)
    for a in result:
        assert a.detected_at >= since


def test_anomaly_has_required_fields():
    result = get_anomalies()
    for a in result:
        assert a.anomaly_id
        assert a.type in ("incident", "closure", "demand_surge")
        assert a.severity in ("low", "medium", "high")


def test_anomaly_incident_and_occupancy_branches():
    """Cover detector branches: incident flag and occupancy_pct > 85."""
    edges = [
        NetworkEdge(edge_id="e1", from_node="n1", to_node="n2", mode="road", incident=True),
        NetworkEdge(edge_id="e2", from_node="n2", to_node="n3", mode="road", occupancy_pct=90.0),
    ]
    snap = DigitalTwinSnapshot(nodes=[], edges=edges)
    with patch("anomaly_detection.detector.get_assembled_snapshot", return_value=snap):
        result = get_anomalies()
    assert len(result) >= 1
    types = {a.type for a in result}
    assert "incident" in types or "demand_surge" in types


def test_anomaly_segment_ids_filter():
    """Cover segment_ids filter: only edges in segment_ids."""
    edges = [
        NetworkEdge(edge_id="e1", from_node="n1", to_node="n2", mode="road", incident=True),
        NetworkEdge(edge_id="e2", from_node="n2", to_node="n3", mode="road"),
    ]
    snap = DigitalTwinSnapshot(nodes=[], edges=edges)
    with patch("anomaly_detection.detector.get_assembled_snapshot", return_value=snap):
        result = get_anomalies(segment_ids=["e1"])
    assert all(a.segment_ids == ["e1"] for a in result)

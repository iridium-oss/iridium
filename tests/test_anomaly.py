"""Anomaly detection tests."""

import sys
from pathlib import Path
from datetime import datetime, timedelta

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/digital-twin", "services/anomaly-detection"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from anomaly_detection.detector import get_anomalies


def test_get_anomalies_returns_list():
    result = get_anomalies()
    assert isinstance(result, list)


def test_get_anomalies_since_filter():
    since = datetime.utcnow() - timedelta(hours=1)
    result = get_anomalies(since=since)
    for a in result:
        assert a.detected_at >= since


def test_anomaly_has_required_fields():
    result = get_anomalies()
    for a in result:
        assert a.anomaly_id
        assert a.type in ("incident", "closure", "demand_surge")
        assert a.severity in ("low", "medium", "high")

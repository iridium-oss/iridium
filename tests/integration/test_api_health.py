"""Integration test: API health and version via FastAPI TestClient."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "packages" / "schemas"))
for p in ("services/digital-twin", "services/forecasting", "services/routing", "services/equity", "services/anomaly-detection", "services/ingestion"):
    path = root / p
    if path.exists():
        sys.path.insert(0, str(path))
sys.path.insert(0, str(root / "apps" / "api"))

from datetime import datetime
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app
from app.api.ingestion import post_ingestion_events
from iridium_schemas.events import IngestionEventBatch, SensorEvent

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"


def test_version():
    r = client.get("/version")
    assert r.status_code == 200
    data = r.json()
    assert "app_version" in data
    assert data.get("service") == "iridium-api"


def test_network_graph():
    r = client.get("/api/v1/network/graph")
    assert r.status_code == 200
    data = r.json()
    assert "nodes" in data
    assert "edges" in data


def test_forecast_congestion():
    r = client.get("/api/v1/forecast/congestion?horizon_minutes=60")
    assert r.status_code == 200
    data = r.json()
    assert data.get("horizon_minutes") == 60
    assert "segments" in data


def test_routing_plan():
    r = client.post(
        "/api/v1/routing/plan",
        json={
            "origin_lat": 40.4093,
            "origin_lon": 49.8671,
            "destination_lat": 40.413,
            "destination_lon": 49.871,
            "optimize": "time",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "alternatives" in data


def test_equity_score():
    r = client.get("/api/v1/equity/score")
    assert r.status_code == 200
    data = r.json()
    assert "districts" in data


def test_anomalies():
    r = client.get("/api/v1/anomalies")
    assert r.status_code == 200
    data = r.json()
    assert "anomalies" in data


def test_ingestion_events_validate():
    r = client.post(
        "/api/v1/ingestion/events",
        json={"sensor_events": [], "gnss_points": [], "weather": [], "public_events": [], "energy_signals": []},
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("accepted") == 0


def test_ingestion_events_validation_error():
    """Cover ingestion 400 path: batch that passes Pydantic but fails validate_batch."""
    bad = IngestionEventBatch.model_construct(
        sensor_events=[SensorEvent.model_construct(segment_id="e1", timestamp=datetime.now(), speed_kmh=300)]
    )
    with pytest.raises(HTTPException) as exc_info:
        post_ingestion_events(bad)
    assert exc_info.value.status_code == 400
    assert "validation_errors" in exc_info.value.detail


def test_value_error_handler():
    # Trigger ValueError from inside /version by making get_settings (used there) raise.
    with patch("app.api.version.get_settings") as mock_settings:
        mock_settings.side_effect = ValueError("Test Error")
        r = client.get("/version")
        assert r.status_code == 400
        assert r.json()["error"]["code"] == "invalid_value"

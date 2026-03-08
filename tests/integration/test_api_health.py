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

from fastapi.testclient import TestClient
from app.main import app

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

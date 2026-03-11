"""Tests for system and weather API endpoints. No fabricated data."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "packages" / "schemas"))
sys.path.insert(0, str(root / "apps" / "api"))

from app.main import app

client = TestClient(app)


def test_system_status():
    r = client.get("/api/v1/system/status")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data or "environment" in data


def test_system_data_sources():
    r = client.get("/api/v1/system/data-sources")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, (dict, list))


def test_system_data_provenance():
    r = client.get("/api/v1/system/data-provenance")
    assert r.status_code == 200
    data = r.json()
    assert "policy" in data or "fields" in data or "sources" in data or "provenance" in data


def test_weather_current():
    r = client.get("/api/v1/weather/current")
    assert r.status_code == 200
    data = r.json()
    assert "data_status" in data
    assert "source_provenance" in data
    assert "snapshots" in data


def test_weather_status():
    r = client.get("/api/v1/weather/status")
    assert r.status_code == 200
    data = r.json()
    assert data.get("provider_id") == "open_meteo"
    assert "data_status" in data
    assert "source_status" in data


def test_weather_history():
    r = client.get("/api/v1/weather/history")
    assert r.status_code == 200
    data = r.json()
    assert "data_status" in data
    assert "source_provenance" in data
    assert "observations" in data
    assert data.get("data_status") in ("unavailable", "live", "recorded_real_snapshot")


def test_system_providers_list():
    r = client.get("/api/v1/system/providers")
    assert r.status_code == 200
    data = r.json()
    assert "providers" in data
    assert "total" in data
    assert isinstance(data["providers"], list)
    assert data["total"] >= 1
    first = data["providers"][0]
    assert "id" in first
    assert "display_name" in first
    assert "source_family" in first
    assert "source_status" in first
    assert "capabilities" in first


def test_system_providers_get():
    r = client.get("/api/v1/system/providers/open_meteo")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "open_meteo"
    assert data["display_name"] == "Open-Meteo"


def test_system_providers_get_404():
    r = client.get("/api/v1/system/providers/nonexistent_provider_xyz")
    assert r.status_code == 404


def test_system_providers_health():
    r = client.get("/api/v1/system/providers/open_meteo/health")
    assert r.status_code == 200
    data = r.json()
    assert "provider_id" in data
    assert "validation_status" in data


def test_system_providers_verify():
    r = client.post("/api/v1/system/providers/open_meteo/verify", json={})
    assert r.status_code == 200
    data = r.json()
    assert "validation_status" in data
    assert "provider_id" in data


def test_system_integrations_status():
    r = client.get("/api/v1/system/integrations/status")
    assert r.status_code == 200
    data = r.json()
    assert "domains" in data or "total_providers" in data


def test_system_integrations_report():
    r = client.get("/api/v1/system/integrations/report")
    assert r.status_code == 200
    data = r.json()
    assert "report_generated_at" in data
    assert "providers" in data
    assert isinstance(data["providers"], list)

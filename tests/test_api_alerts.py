"""Tests for alerts API. Alerts come from real provider fetchers; no fabricated alerts."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "packages" / "schemas"))
sys.path.insert(0, str(root / "apps" / "api"))

from app.main import app
from iridium_schemas.transit import Alert

client = TestClient(app)


@patch("app.api.alerts._fetch_transit_alerts")
def test_alerts_list(mock_fetch):
    mock_fetch.return_value = []
    r = client.get("/api/v1/alerts")
    assert r.status_code == 200
    data = r.json()
    assert "alerts" in data
    assert "note" in data
    assert isinstance(data["alerts"], list)


@patch("app.api.alerts._fetch_transit_alerts")
def test_alerts_list_with_filter(mock_fetch):
    mock_fetch.return_value = []
    r = client.get("/api/v1/alerts?provider=bakumetro_official_alerts")
    assert r.status_code == 200
    data = r.json()
    assert "alerts" in data


def test_alerts_get_by_id():
    with patch("app.api.alerts._fetch_transit_alerts") as mock:
        mock.return_value = [
            Alert(
                alert_id="test-1",
                title="Test alert",
                provider="test",
                source_provider="test",
                source_status="official",
            )
        ]
        r = client.get("/api/v1/alerts/test-1")
        assert r.status_code == 200
        data = r.json()
        assert data.get("alert", {}).get("alert_id") == "test-1"


def test_alerts_get_by_id_not_found():
    with patch("app.api.alerts._fetch_transit_alerts") as mock:
        mock.return_value = []
        r = client.get("/api/v1/alerts/nonexistent")
        assert r.status_code == 404

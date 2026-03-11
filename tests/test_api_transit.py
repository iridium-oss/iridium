"""
Comprehensive tests for Transit API endpoints to reach 100% coverage.
Mocks all infrastructure dependencies to isolate API logic.
"""

import sys
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "packages" / "schemas"))
sys.path.insert(0, str(root / "apps" / "api"))

from app.main import app
from iridium_schemas.transit import (
    Alert,
    SourceStatus,
    TransitRoute,
    TransitStop,
)

client = TestClient(app)


@pytest.fixture
def mock_registry():
    with patch("app.api.transit._get_registry") as mock:
        entry = MagicMock()
        entry.provider_id = "test_provider"
        entry.name = "Test Provider"
        entry.status = "live"
        entry.feed_url = "http://test.com"
        entry.note = "Test note"
        entry.updated_at = datetime(2026, 3, 8, tzinfo=UTC)
        mock.return_value = [entry]
        yield mock


@pytest.fixture
def mock_snapshot():
    with patch("app.api.transit._build_snapshot") as mock:
        yield mock


def test_get_providers(mock_registry):
    response = client.get("/api/v1/transit/providers")
    assert response.status_code == 200
    data = response.json()
    assert len(data["providers"]) == 1
    assert data["providers"][0]["provider_id"] == "test_provider"


def test_get_providers_calls_registry():
    """Cover _get_registry() body by patching at source so the real function runs."""
    with patch("transit_ingestion.registry.get_provider_registry") as mock_reg:
        mock_reg.return_value = []
        response = client.get("/api/v1/transit/providers")
        assert response.status_code == 200
        mock_reg.assert_called_once()


def test_get_routes(mock_snapshot):
    mock_snapshot.return_value = {
        "routes": [
            TransitRoute(
                route_id="r1",
                agency_id="a1",
                short_name="5",
                long_name="Route 5",
                route_type="3",
                source_provider="test",
                source_status="live",
            )
        ]
    }
    response = client.get("/api/v1/transit/routes?bakubus_limit=5")
    assert response.status_code == 200
    assert len(response.json()["routes"]) == 1


def test_get_routes_empty(mock_snapshot):
    mock_snapshot.return_value = {}
    response = client.get("/api/v1/transit/routes")
    assert response.status_code == 200
    assert response.json()["routes"] == []


def test_get_stops(mock_snapshot):
    mock_snapshot.return_value = {
        "stops": [
            TransitStop(
                stop_id="s1",
                name="Stop 1",
                lat=40.4,
                lon=49.9,
                source_provider="test",
                source_status="live",
            )
        ]
    }
    response = client.get("/api/v1/transit/stops")
    assert response.status_code == 200
    assert len(response.json()["stops"]) == 1


def test_get_network(mock_snapshot):
    mock_snapshot.return_value = {
        "agencies": [1],
        "routes": [1],
        "stops": [1, 2],
        "variants": [1],
        "shapes": [1],
        "interchanges": [],
        "metadata": {"key": "val"},
    }
    response = client.get("/api/v1/transit/network")
    assert response.status_code == 200
    data = response.json()
    assert data["stops"] == 2
    assert data["metadata"]["key"] == "val"


def test_get_readiness():
    with patch("transit_ingestion.validation.readiness.compute_readiness_report") as mock_report:
        report = MagicMock()
        report.static_stop_discovery = True
        report.route_visualization = True
        report.transfer_graph = False
        report.timetable_routing = False
        report.missing_for_otp = ["test"]
        report.provider_capabilities = {}
        mock_report.return_value = report

        with (
            patch("transit_ingestion.normalization.merge.build_unified_transit_snapshot"),
            patch("transit_ingestion.providers.bakumetro_official.build_static_metro_network"),
        ):
            response = client.get("/api/v1/transit/readiness")
            assert response.status_code == 200
            assert response.json()["static_stop_discovery"] is True


def test_get_gtfs_status():
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.__truediv__") as mock_div,
    ):
        mock_div.return_value.exists.return_value = True
        response = client.get("/api/v1/transit/gtfs/status")
        assert response.status_code == 200
        assert response.json()["built"] is True


def test_get_gtfs_status_not_built():
    with patch("pathlib.Path.exists", return_value=False):
        response = client.get("/api/v1/transit/gtfs/status")
        assert response.status_code == 200
        assert response.json()["built"] is False


def test_get_alerts():
    alert = Alert(
        alert_id="a1",
        title="Test",
        published_at=datetime.now(UTC),
        provider="test",
        affected_mode="bus",
        alert_category="construction",
        severity="warning",
        source_provider="test",
        source_status="live",
    )
    with (
        patch(
            "transit_ingestion.provenance.priority.merge_alerts_by_priority", return_value=[alert]
        ),
        patch("transit_ingestion.providers.bakubus_official_alerts.fetch_bakubus_alerts"),
        patch("transit_ingestion.providers.bakumetro_official_alerts.fetch_metro_alerts"),
    ):
        response = client.get("/api/v1/transit/alerts")
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 1


def test_get_predicted_arrivals():
    arrival = MagicMock()
    arrival.prediction_id = "p1"
    arrival.predicted_at = datetime.now(UTC)

    status = MagicMock()
    status.stop_id = "s1"
    status.status = "ok"

    with (
        patch("transit_ingestion.providers.yandex_transport_observed.fetch_yandex_stop_page"),
        patch(
            "transit_ingestion.providers.yandex_transport_observed.normalize_yandex_stop_observations",
            return_value=([arrival], [status], []),
        ),
    ):
        response = client.get("/api/v1/transit/predicted-arrivals?stop_url=http://test.com")
        assert response.status_code == 200
        assert len(response.json()["predicted_arrivals"]) == 1


def test_get_realtime_observations():
    with (
        patch("transit_ingestion.providers.yandex_transport_observed.fetch_yandex_stop_page"),
        patch(
            "transit_ingestion.providers.yandex_transport_observed.normalize_yandex_stop_observations",
            return_value=([], [], []),
        ),
        patch("transit_ingestion.providers.yandex_metro_operational.fetch_yandex_metro_page"),
        patch(
            "transit_ingestion.providers.yandex_metro_operational.normalize_yandex_metro_operational",
            return_value=([], []),
        ),
    ):
        response = client.get("/api/v1/transit/realtime-observations")
        assert response.status_code == 200
        assert "stop_statuses" in response.json()


def test_get_provider_priority():
    response = client.get("/api/v1/transit/provider-priority")
    assert response.status_code == 200
    assert "alerts" in response.json()


def test_get_source_status():
    with (
        patch(
            "transit_ingestion.providers.yandex_traffic_context.get_traffic_context_status",
            return_value="live",
        ),
        patch(
            "transit_ingestion.providers.twogis_public_transport.get_twogis_status",
            return_value="configured",
        ),
        patch(
            "transit_ingestion.providers.moovit_partner.get_moovit_status", return_value="available"
        ),
    ):
        response = client.get("/api/v1/transit/source-status")
        assert response.status_code == 200
        assert len(response.json()["providers"]) == 7


def test_build_snapshot_logic():
    from app.api.transit import _build_snapshot

    with (
        patch("transit_ingestion.providers.bakumetro_official.build_static_metro_network"),
        patch("transit_ingestion.providers.bakubus_ayna.fetch_bus_list") as mock_list,
        patch("transit_ingestion.providers.bakubus_ayna.fetch_bus_by_id") as mock_id,
        patch("transit_ingestion.providers.bakubus_ayna.normalize_bakubus_route") as mock_norm,
        patch(
            "transit_ingestion.providers.bakubus_ayna.normalize.normalize_bus_list"
        ) as mock_norm_list,
        patch("transit_ingestion.normalization.merge.build_unified_transit_snapshot") as mock_merge,
    ):

        mock_list.return_value = MagicMock(
            error=None, data=[{"id": "1"}], fetched_at=datetime.now(UTC)
        )
        mock_id.return_value = MagicMock(
            error=None, data={"detail": "data"}, fetched_at=datetime.now(UTC)
        )
        mock_norm.return_value = (None, None, None, [], [], [], None)
        mock_norm_list.return_value = [{"id": "1"}]

        _build_snapshot(bakubus_limit=1)
        assert mock_list.called
        assert mock_id.called
        mock_merge.assert_called_once()
        # bakubus_routes should contain one entry (append branch covered)
        call_kw = mock_merge.call_args[1]
        assert call_kw.get("bakubus_routes") is not None
        assert len(call_kw["bakubus_routes"]) == 1


def test_partner_routes_structure():
    """GET /transit/partner-routes returns alternatives and providers_used; empty when no credentials."""
    response = client.get(
        "/api/v1/transit/partner-routes",
        params={"from_lat": 40.4093, "from_lon": 49.8671, "to_lat": 40.3764, "to_lon": 49.8530},
    )
    assert response.status_code == 200
    data = response.json()
    assert "alternatives" in data
    assert "providers_used" in data
    assert "note" in data
    assert isinstance(data["alternatives"], list)
    assert isinstance(data["providers_used"], list)


def test_partner_routes_with_mock_twogis():
    """With 2GIS configured (mocked), partner-routes can return alternatives."""
    from iridium_schemas.transit import SourceFamily, TransitPartnerRouteResult

    with (
        patch(
            "transit_ingestion.providers.twogis_public_transport.get_twogis_status",
            return_value="configured",
        ),
        patch(
            "transit_ingestion.providers.twogis_public_transport.fetch_route_alternatives"
        ) as mock_fetch,
    ):
        mock_fetch.return_value = [
            TransitPartnerRouteResult(
                result_id="twogis_1",
                total_duration_seconds=1200,
                transfer_count=1,
                route_variants=[],
                schedules_returned=True,
                observed_at=datetime.now(UTC),
                source_provider="twogis_public_transport",
                source_family=SourceFamily.LICENSED_API.value,
                source_status=SourceStatus.LICENSED_PARTNER.value,
                confidence="licensed_partner",
                validation_note="From 2GIS API",
            )
        ]
        response = client.get(
            "/api/v1/transit/partner-routes",
            params={"from_lat": 40.41, "from_lon": 49.87, "to_lat": 40.37, "to_lon": 49.85},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["alternatives"]) >= 1
        assert "twogis_public_transport" in data["providers_used"]

"""
Tests for Baku transit integration: AYNA parsing, BakuBus normalization, metro static network, readiness.
No network calls in tests unless explicitly mocked.
"""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/transit-ingestion"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from datetime import UTC

from iridium_schemas.transit import (
    SourceFamily,
    SourceStatus,
    TransitAgency,
    TransitStop,
)


class TestBakubusNormalize:
    """BakuBus AYNA response normalization."""

    def test_normalize_bus_list_empty(self):
        from transit_ingestion.providers.bakubus_ayna.normalize import normalize_bus_list

        assert normalize_bus_list(None) == []
        assert normalize_bus_list([]) == []

    def test_normalize_bus_list_from_list(self):
        from transit_ingestion.providers.bakubus_ayna.normalize import normalize_bus_list

        raw = [{"id": "1", "number": "5"}, {"busId": "2", "number": "12"}]
        out = normalize_bus_list(raw)
        assert len(out) == 2
        assert out[0]["id"] == "1"
        assert out[1]["id"] == "2"

    def test_normalize_bakubus_route_none(self):
        from transit_ingestion.providers.bakubus_ayna.normalize import normalize_bakubus_route

        ag, r, v, stops, seq, shapes, fp = normalize_bakubus_route(None)
        assert ag is None
        assert r is None
        assert v is None
        assert stops == []
        assert seq == []
        assert shapes == []
        assert fp is None

    def test_normalize_bakubus_route_minimal(self):
        from transit_ingestion.providers.bakubus_ayna.normalize import normalize_bakubus_route

        raw = {
            "id": "42",
            "number": "18",
            "carrier": "BakuBus",
            "firstPoint": "A",
            "lastPoint": "B",
            "stops": [{"id": "s1", "name": "Stop 1", "lat": 40.4, "lon": 49.9}],
            "flowCoordinates": [[40.4, 49.9], [40.41, 49.91]],
        }
        ag, r, v, stops, seq, shapes, fp = normalize_bakubus_route(raw)
        assert ag is not None
        assert ag.agency_id == "bakubus"
        assert r is not None
        assert r.route_id == "bakubus_42"
        assert r.short_name == "18"
        assert v is not None
        assert v.first_point == "A"
        assert v.last_point == "B"
        assert len(stops) == 1
        assert stops[0].name == "Stop 1"
        assert stops[0].lat == 40.4
        assert len(seq) == 1
        assert len(shapes) == 2
        assert ag.source_provider == "bakubus_ayna"
        assert ag.source_status == SourceStatus.PUBLIC_UNDOCUMENTED.value


class TestBakumetroStatic:
    """Baku Metro static network."""

    def test_metro_agency(self):
        from transit_ingestion.providers.bakumetro_official.static_network import get_metro_agency

        a = get_metro_agency()
        assert a.agency_id == "baku_metro"
        assert a.source_provider == "bakumetro_official"
        assert a.source_status == SourceStatus.STATIC_SCHEDULE_ONLY.value

    def test_metro_lines(self):
        from transit_ingestion.providers.bakumetro_official.static_network import get_metro_lines

        lines = get_metro_lines()
        assert len(lines) >= 3
        ids = {r.route_id for r in lines}
        assert "bakumetro_red" in ids
        assert "bakumetro_green" in ids
        assert "bakumetro_purple" in ids

    def test_metro_stations(self):
        from transit_ingestion.providers.bakumetro_official.static_network import get_metro_stations

        stops = get_metro_stations()
        assert len(stops) > 0
        for s in stops:
            assert s.source_provider == "bakumetro_official"
            assert s.lat is None
            assert s.lon is None

    def test_build_static_metro_network(self):
        from transit_ingestion.providers.bakumetro_official import build_static_metro_network

        net = build_static_metro_network()
        assert "agency" in net
        assert "routes" in net
        assert "stops" in net
        assert "metadata" in net
        assert net["metadata"]["timetable_available"] is False


class TestReadiness:
    """Readiness report."""

    def test_readiness_metro_only(self):
        from transit_ingestion.normalization.merge import build_unified_transit_snapshot
        from transit_ingestion.providers.bakumetro_official import build_static_metro_network
        from transit_ingestion.validation.readiness import compute_readiness_report

        snapshot = build_unified_transit_snapshot(bakumetro_network=build_static_metro_network())
        report = compute_readiness_report(snapshot)
        assert report.static_stop_discovery is True
        assert report.route_visualization is True
        assert report.timetable_routing is False
        assert (
            "stop_times" in str(report.missing_for_otp).lower()
            or "timetable" in str(report.missing_for_otp).lower()
        )


class TestCanonicalSchema:
    """Canonical transit schema validation."""

    def test_transit_agency_required_fields(self):
        a = TransitAgency(
            agency_id="test_agency",
            name="Test Agency",
            source_provider="test",
            source_family="public_api",
            source_status="public_undocumented",
        )
        assert a.agency_id == "test_agency"
        assert a.name == "Test Agency"
        assert a.source_provider == "test"

    def test_transit_stop_with_coords(self):
        s = TransitStop(
            stop_id="s1",
            name="Stop One",
            lat=40.4,
            lon=49.9,
            source_provider="bakubus_ayna",
            source_family=SourceFamily.PUBLIC_API.value,
            source_status=SourceStatus.PUBLIC_UNDOCUMENTED.value,
        )
        assert s.stop_id == "s1"
        assert s.lat == 40.4
        assert s.lon == 49.9

    def test_source_family_enum(self):
        assert SourceFamily.PUBLIC_UNDOCUMENTED.value == "public_undocumented"
        assert SourceStatus.STATIC_SCHEDULE_ONLY.value == "static_schedule_only"


class TestGtfsBuilder:
    """GTFS builder produces only defensible files."""

    def test_build_gtfs_static_writes_core_files(self, tmp_path):
        from transit_ingestion.gtfs_builder.build import build_gtfs_static
        from transit_ingestion.normalization.merge import build_unified_transit_snapshot
        from transit_ingestion.providers.bakumetro_official import build_static_metro_network

        net = build_static_metro_network()
        snapshot = build_unified_transit_snapshot(bakumetro_network=net)
        out = build_gtfs_static(snapshot, output_dir=tmp_path)
        assert (out / "agency.txt").exists()
        assert (out / "routes.txt").exists()
        assert (out / "stops.txt").exists()
        assert (out / "README.txt").exists()
        assert "Repository-generated" in (out / "README.txt").read_text()
        assert "Not operator-issued" in (out / "README.txt").read_text()

    def test_build_gtfs_static_no_stop_times(self, tmp_path):
        from transit_ingestion.gtfs_builder.build import build_gtfs_static
        from transit_ingestion.normalization.merge import build_unified_transit_snapshot
        from transit_ingestion.providers.bakumetro_official import build_static_metro_network

        snapshot = build_unified_transit_snapshot(bakumetro_network=build_static_metro_network())
        out = build_gtfs_static(snapshot, output_dir=tmp_path)
        assert not (out / "stop_times.txt").exists()
        assert not (out / "trips.txt").exists()


class TestProviderStatus:
    """Provider registry and status reporting."""

    def test_registry_returns_bakubus_ayna_and_bakumetro(self):
        from transit_ingestion.registry import get_provider_registry

        entries = get_provider_registry()
        ids = [e.provider_id for e in entries]
        assert "bakubus_ayna" in ids
        assert "bakumetro_official" in ids

    def test_registry_live_status(self):
        from transit_ingestion.registry import get_provider_registry

        entries = get_provider_registry()
        bakubus = next(e for e in entries if e.provider_id == "bakubus_ayna")
        metro = next(e for e in entries if e.provider_id == "bakumetro_official")
        assert bakubus.status == "live"
        assert metro.status == "live"

    def test_registry_permission_required_for_operator_gtfs(self):
        from transit_ingestion.registry import get_provider_registry

        entries = get_provider_registry()
        baku_metro = next(e for e in entries if e.provider_id == "baku_metro")
        assert baku_metro.status == "permission_required"


class TestOsmResolution:
    """OSM station resolution and ambiguous-match validation. No live network in tests."""

    def test_resolve_station_empty_name_returns_none_confidence(self):
        from datetime import datetime

        from transit_ingestion.providers.bakumetro_official.osm_resolution import resolve_station

        # Stop with empty name and empty stop_id so no Nominatim call is made.
        stop = TransitStop(
            stop_id="",
            name="",
            lat=None,
            lon=None,
            source_provider="bakumetro_official",
            source_family="official_website",
            source_status="static_schedule_only",
            fetched_at=datetime.now(UTC),
        )
        res = resolve_station(stop)
        assert res.confidence == "none"
        assert res.stop.lat is None
        assert res.stop.lon is None

    def test_flag_ambiguous_returns_ambiguous_ids(self):
        from transit_ingestion.providers.bakumetro_official import (
            OsmValidationReport,
            flag_ambiguous_for_manual_review,
        )

        report = OsmValidationReport(
            ambiguous_stop_ids=["bakumetro_red_1_Station_A"],
            unresolved_stop_ids=["bakumetro_red_2_Station_B"],
            resolved_count=5,
        )
        review = flag_ambiguous_for_manual_review(report)
        assert "bakumetro_red_1_Station_A" in review
        assert len(review) == 1

    def test_resolve_metro_stations_with_mock_no_candidates(self):
        from datetime import datetime
        from unittest.mock import patch

        from transit_ingestion.providers.bakumetro_official import osm_resolution
        from transit_ingestion.providers.bakumetro_official.osm_resolution import (
            resolve_metro_stations,
        )

        t = datetime.now(UTC)
        stops = [
            TransitStop(
                stop_id="test_1",
                name="TestStation",
                lat=None,
                lon=None,
                source_provider="bakumetro_official",
                source_family="official_website",
                source_status="static_schedule_only",
                fetched_at=t,
            ),
        ]
        with patch.object(osm_resolution, "_search_nominatim", return_value=[]):
            resolved, report = resolve_metro_stations(stops, timeout=0.1)
        assert len(resolved) == 1
        assert resolved[0].lat is None
        assert resolved[0].lon is None
        assert "test_1" in report.unresolved_stop_ids

    def test_resolve_station_single_candidate_high_confidence(self):
        from datetime import datetime
        from unittest.mock import patch

        from transit_ingestion.providers.bakumetro_official import osm_resolution
        from transit_ingestion.providers.bakumetro_official.osm_resolution import resolve_station

        stop = TransitStop(
            stop_id="test_s1",
            name="28 May",
            lat=None,
            lon=None,
            source_provider="bakumetro_official",
            source_family="official_website",
            source_status="static_schedule_only",
            fetched_at=datetime.now(UTC),
        )
        with patch.object(
            osm_resolution, "_search_nominatim", return_value=[{"lat": "40.4093", "lon": "49.8671"}]
        ):
            res = resolve_station(stop)
        assert res.confidence == "high"
        assert res.stop.lat == 40.4093
        assert res.stop.lon == 49.8671
        assert res.stop.osm_match_confidence == "high"


class TestOfficialAlerts:
    """Official BakuBus and Baku Metro alert parsing."""

    def test_normalize_bakubus_alerts_empty_on_error(self):
        from datetime import datetime

        from transit_ingestion.providers.bakubus_official_alerts.fetcher import FetchedPage
        from transit_ingestion.providers.bakubus_official_alerts.normalize import (
            normalize_bakubus_alerts,
        )

        fetched = FetchedPage(
            url="https://bakubus.az",
            html="",
            fetched_at=datetime.now(UTC),
            status_code=200,
            error="fail",
        )
        assert normalize_bakubus_alerts(fetched) == []

    def test_normalize_bakubus_alerts_extracts_links(self):
        from datetime import datetime

        from transit_ingestion.providers.bakubus_official_alerts.fetcher import FetchedPage
        from transit_ingestion.providers.bakubus_official_alerts.normalize import (
            normalize_bakubus_alerts,
        )

        html = '<a href="/az/news/1">Route 5 change</a><a href="https://bakubus.az/az/news/2">Interval update</a>'
        fetched = FetchedPage(
            url="https://bakubus.az/az/news",
            html=html,
            fetched_at=datetime.now(UTC),
            status_code=200,
            error=None,
        )
        alerts = normalize_bakubus_alerts(fetched)
        assert len(alerts) >= 2
        assert all(a.source_provider == "bakubus_official_alerts" for a in alerts)
        assert all(a.source_status == "official_alerts_only" for a in alerts)

    def test_normalize_metro_alerts_empty_on_error(self):
        from datetime import datetime

        from transit_ingestion.providers.bakumetro_official_alerts.fetcher import FetchedMetroPage
        from transit_ingestion.providers.bakumetro_official_alerts.normalize import (
            normalize_metro_alerts,
        )

        fetched = FetchedMetroPage(
            url="https://metro.gov.az",
            html="",
            fetched_at=datetime.now(UTC),
            status_code=500,
            error="fail",
        )
        assert normalize_metro_alerts(fetched) == []


class TestYandexObserved:
    """Yandex stop-page predicted arrival and observation normalization."""

    def test_normalize_yandex_extracts_arrival_hints(self):
        from datetime import datetime

        from transit_ingestion.providers.yandex_transport_observed.fetcher import FetchedYandexPage
        from transit_ingestion.providers.yandex_transport_observed.normalize import (
            normalize_yandex_stop_observations,
        )

        html = "Bus in 5 min and 12 minutes."
        fetched = FetchedYandexPage(
            url="https://yandex.az/maps",
            html=html,
            fetched_at=datetime.now(UTC),
            status_code=200,
            error=None,
        )
        arrivals, statuses, _ = normalize_yandex_stop_observations(fetched, stop_id="test_stop")
        assert len(arrivals) >= 2
        assert all(a.source_status == "public_web_observed" for a in arrivals)

    def test_normalize_yandex_empty_page_returns_stop_status_unknown(self):
        from datetime import datetime

        from transit_ingestion.providers.yandex_transport_observed.fetcher import FetchedYandexPage
        from transit_ingestion.providers.yandex_transport_observed.normalize import (
            normalize_yandex_stop_observations,
        )

        fetched = FetchedYandexPage(
            url="https://yandex.az/maps",
            html="<div>no minutes</div>",
            fetched_at=datetime.now(UTC),
            status_code=200,
            error=None,
        )
        arrivals, statuses, _ = normalize_yandex_stop_observations(fetched)
        assert len(arrivals) == 0
        assert len(statuses) == 1
        assert statuses[0].status == "unknown"


class TestMetroOperational:
    """Yandex metro operational notice normalization."""

    def test_normalize_metro_operational_extracts_closed_hints(self):
        from datetime import datetime

        from transit_ingestion.providers.yandex_metro_operational.fetcher import FetchedMetroPage
        from transit_ingestion.providers.yandex_metro_operational.normalize import (
            normalize_yandex_metro_operational,
        )

        html = "Station closed for maintenance. Entrance closed."
        fetched = FetchedMetroPage(
            url="https://yandex.az/maps/metro",
            html=html,
            fetched_at=datetime.now(UTC),
            status_code=200,
            error=None,
        )
        notices, constraints = normalize_yandex_metro_operational(fetched)
        assert len(notices) >= 1
        assert all(n.source_status == "public_web_operational_context" for n in notices)


class TestProviderPriority:
    """Source priority logic."""

    def test_alert_priority_order(self):
        from transit_ingestion.provenance.priority import get_alert_priority_order

        order = get_alert_priority_order()
        assert "bakubus_official_alerts" in order
        assert "bakumetro_official_alerts" in order
        assert order.index("bakubus_official_alerts") < order.index("moovit_partner")

    def test_merge_alerts_by_priority(self):
        from datetime import datetime

        from iridium_schemas.transit import Alert
        from transit_ingestion.provenance.priority import merge_alerts_by_priority

        t = datetime.now(UTC)
        a1 = Alert(
            alert_id="id1",
            title="Bus",
            source_provider="bakubus_official_alerts",
            source_family="",
            source_status="",
        )
        a2 = Alert(
            alert_id="id2",
            title="Metro",
            source_provider="bakumetro_official_alerts",
            source_family="",
            source_status="",
        )
        merged = merge_alerts_by_priority(
            [
                ("moovit_partner", [a2]),
                ("bakubus_official_alerts", [a1]),
            ]
        )
        assert len(merged) == 2
        assert merged[0].source_provider == "bakubus_official_alerts"
        assert merged[1].source_provider == "bakumetro_official_alerts"


class TestSourceStatus:
    """Source-status truthfulness."""

    def test_yandex_traffic_status(self):
        from transit_ingestion.providers.yandex_traffic_context import get_traffic_context_status

        status = get_traffic_context_status()
        assert status in ("web_observed", "licensed_api", "unavailable")

    def test_twogis_status(self):
        from transit_ingestion.providers.twogis_public_transport import get_twogis_status

        status = get_twogis_status()
        assert status in ("configured", "unavailable")

    def test_moovit_status(self):
        from transit_ingestion.providers.moovit_partner import get_moovit_status

        status = get_moovit_status()
        assert status in ("available", "partner_required")

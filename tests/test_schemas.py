"""Schema validation tests."""

import pytest
from datetime import datetime
from pydantic import ValidationError

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "packages" / "schemas"))
sys.path.insert(0, str(root / "services" / "digital-twin"))

from iridium_schemas.events import SensorEvent, IngestionEventBatch
from iridium_schemas.routing import RouteRequest, RouteResponse
from iridium_schemas.forecast import CongestionForecastResponse, ForecastSegment
from iridium_schemas.equity import DistrictScore, MobilityEquityScore
from iridium_schemas.anomaly import AnomalyEvent


def test_sensor_event_valid():
    e = SensorEvent(segment_id="e1", timestamp=datetime.now(timezone.utc), speed_kmh=30.0)
    assert e.segment_id == "e1"
    assert e.speed_kmh == 30.0


def test_sensor_event_invalid_speed():
    with pytest.raises(ValidationError):
        SensorEvent(segment_id="e1", timestamp=datetime.now(timezone.utc), speed_kmh=300)


def test_ingestion_batch_empty():
    b = IngestionEventBatch()
    assert b.sensor_events == []
    assert len(b.gnss_points) == 0


def test_route_request_valid():
    r = RouteRequest(origin_lat=40.4, origin_lon=49.8, destination_lat=40.5, destination_lon=49.9)
    assert r.optimize == "time"


def test_route_request_invalid_lat():
    with pytest.raises(ValidationError):
        RouteRequest(origin_lat=100, origin_lon=49.8, destination_lat=40.5, destination_lon=49.9)


def test_forecast_segment():
    s = ForecastSegment(segment_id="e1", timestamp=datetime.now(timezone.utc), congestion_score=0.5)
    assert s.congestion_score == 0.5


def test_district_score():
    d = DistrictScore(district_id="d1", composite_score=0.7)
    assert d.district_id == "d1"


def test_anomaly_event():
    a = AnomalyEvent(anomaly_id="a1", type="incident", severity="high", detected_at=datetime.now(timezone.utc))
    assert a.type == "incident"

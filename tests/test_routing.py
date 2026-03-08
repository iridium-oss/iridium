"""Routing service tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/digital-twin", "services/routing"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from iridium_schemas.routing import RouteRequest
from routing.plan import plan_routes


def test_plan_routes_returns_response():
    req = RouteRequest(
        origin_lat=40.4093,
        origin_lon=49.8671,
        destination_lat=40.413,
        destination_lon=49.871,
    )
    res = plan_routes(req)
    assert res.alternatives is not None
    assert len(res.alternatives) >= 1


def test_plan_routes_alternative_has_segments():
    req = RouteRequest(origin_lat=40.4093, origin_lon=49.8671, destination_lat=40.413, destination_lon=49.871)
    res = plan_routes(req)
    alt = res.alternatives[0]
    assert alt.total_duration_min >= 0
    assert alt.segments is not None

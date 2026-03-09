"""
Transit API: providers, routes, stops, network, readiness, GTFS status.
BakuBus (AYNA) and Baku Metro (official) integrated. No fabricated data.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Query

router = APIRouter()


def _get_registry():
    from transit_ingestion.registry import get_provider_registry
    return get_provider_registry()


def _build_snapshot(bakubus_limit: int = 0):
    """Build unified snapshot. Metro always; BakuBus if bakubus_limit > 0 (fetch from AYNA)."""
    from transit_ingestion.providers.bakumetro_official import build_static_metro_network
    from transit_ingestion.providers.bakubus_ayna import fetch_bus_list, fetch_bus_by_id, normalize_bakubus_route
    from transit_ingestion.normalization.merge import build_unified_transit_snapshot

    metro = build_static_metro_network(datetime.now(timezone.utc))
    bakubus_routes = []
    if bakubus_limit > 0:
        list_result = fetch_bus_list(timeout=15.0, cache_raw=True)
        if list_result.error is None and list_result.data:
            from transit_ingestion.providers.bakubus_ayna.normalize import normalize_bus_list
            ids = normalize_bus_list(list_result.data, list_result.fetched_at)
            for item in ids[:bakubus_limit]:
                bid = item.get("id")
                if bid is None:  # pragma: no cover
                    continue
                detail = fetch_bus_by_id(str(bid), timeout=10.0, cache_raw=True)
                if detail.error is None and detail.data:
                    ag, r, v, stops, seq, shapes, fp = normalize_bakubus_route(
                        detail.data, detail.fetched_at
                    )
                    bakubus_routes.append({
                        "agency": ag, "route": r, "variant": v,
                        "stops": stops, "stop_sequence": seq, "shape_points": shapes,
                        "fare_policy": fp,
                    })
    return build_unified_transit_snapshot(
        bakubus_routes=bakubus_routes if bakubus_routes else None,
        bakumetro_network=metro,
    )


@router.get(
    "/transit/providers",
    summary="Transit provider registry",
    description="Provider list with status (live, permission_required). BakuBus AYNA and Baku Metro official are integrated.",
)
def get_providers():
    registry = _get_registry()
    return {
        "providers": [
            {
                "provider_id": e.provider_id,
                "name": e.name,
                "status": e.status,
                "feed_url": e.feed_url,
                "note": e.note,
                "updated_at": e.updated_at.isoformat() if e.updated_at else None,
            }
            for e in registry
        ],
    }


@router.get(
    "/transit/routes",
    summary="Transit routes",
    description="Unified routes from Baku Metro and BakuBus (AYNA). Optional bakubus_limit to fetch up to N bus routes from AYNA.",
)
def get_routes(bakubus_limit: int = Query(0, ge=0, le=50, description="Max bus routes to fetch from AYNA (0 = metro only)")):
    snapshot = _build_snapshot(bakubus_limit=bakubus_limit)
    routes = snapshot.get("routes") or []
    return {
        "routes": [
            {
                "route_id": r.route_id,
                "agency_id": r.agency_id,
                "short_name": r.short_name,
                "long_name": r.long_name,
                "route_type": r.route_type,
                "source_provider": r.source_provider,
                "source_status": r.source_status,
            }
            for r in routes
        ],
    }


@router.get(
    "/transit/stops",
    summary="Transit stops",
    description="Unified stops. Metro stations; BakuBus stops when bakubus_limit > 0.",
)
def get_stops(bakubus_limit: int = Query(0, ge=0, le=50)):
    snapshot = _build_snapshot(bakubus_limit=bakubus_limit)
    stops = snapshot.get("stops") or []
    return {
        "stops": [
            {
                "stop_id": s.stop_id,
                "name": s.name,
                "lat": s.lat,
                "lon": s.lon,
                "source_provider": s.source_provider,
                "source_status": s.source_status,
            }
            for s in stops
        ],
    }


@router.get(
    "/transit/network",
    summary="Transit network summary",
    description="Agency, route, stop counts and metadata. No fabricated timetable.",
)
def get_network(bakubus_limit: int = Query(0, ge=0, le=50)):
    snapshot = _build_snapshot(bakubus_limit=bakubus_limit)
    return {
        "agencies": len(snapshot.get("agencies") or []),
        "routes": len(snapshot.get("routes") or []),
        "stops": len(snapshot.get("stops") or []),
        "variants": len(snapshot.get("variants") or []),
        "shapes": len(snapshot.get("shapes") or []),
        "interchanges": len(snapshot.get("interchanges") or []),
        "metadata": snapshot.get("metadata") or {},
    }


@router.get(
    "/transit/readiness",
    summary="Transit readiness for OTP",
    description="Static stop discovery, route visualization, transfer graph, timetable routing. Honest about missing stop_times.",
)
def get_readiness():
    from transit_ingestion.providers.bakumetro_official import build_static_metro_network
    from transit_ingestion.normalization.merge import build_unified_transit_snapshot
    from transit_ingestion.validation.readiness import compute_readiness_report

    snapshot = build_unified_transit_snapshot(bakumetro_network=build_static_metro_network())
    report = compute_readiness_report(snapshot)
    return {
        "static_stop_discovery": report.static_stop_discovery,
        "route_visualization": report.route_visualization,
        "transfer_graph": report.transfer_graph,
        "timetable_routing": report.timetable_routing,
        "missing_for_otp": report.missing_for_otp,
        "provider_capabilities": report.provider_capabilities,
    }


@router.get(
    "/transit/gtfs/status",
    summary="GTFS build status",
    description="Whether GTFS was built, label (repository-generated), and path if available.",
)
def get_gtfs_status():
    import os
    from pathlib import Path
    from transit_ingestion.gtfs_builder.build import GTFS_BUILD_LABEL

    out_dir = os.environ.get("IRIDIUM_GTFS_OUTPUT_DIR", "gtfs_output")
    path = Path(out_dir)
    built = path.exists() and (path / "agency.txt").exists()
    return {
        "built": built,
        "label": GTFS_BUILD_LABEL,
        "output_dir": str(path.resolve()) if path.exists() else None,
        "note": "GTFS is repository-generated from official and public sources; not operator-issued.",
    }


def _alert_to_dict(a):
    return {
        "alert_id": a.alert_id,
        "title": a.title,
        "published_at": a.published_at.isoformat() if a.published_at else None,
        "provider": a.provider,
        "affected_mode": a.affected_mode,
        "affected_route_id": a.affected_route_id,
        "affected_station_id": a.affected_station_id,
        "alert_category": a.alert_category,
        "severity": a.severity,
        "source_url": a.source_url,
        "source_provider": a.source_provider,
        "source_family": a.source_family,
        "source_status": a.source_status,
        "observed_at": a.observed_at.isoformat() if a.observed_at else None,
        "confidence": a.confidence,
    }


@router.get(
    "/transit/alerts",
    summary="Transit alerts",
    description="Official and observed alerts merged by source priority. Truthful source metadata.",
)
def get_alerts():
    from transit_ingestion.providers.bakubus_official_alerts import fetch_bakubus_alerts
    from transit_ingestion.providers.bakumetro_official_alerts import fetch_metro_alerts
    from transit_ingestion.provenance.priority import merge_alerts_by_priority, get_alert_priority_order

    bus_alerts = fetch_bakubus_alerts(timeout=15.0)
    metro_alerts = fetch_metro_alerts(timeout=15.0)
    merged = merge_alerts_by_priority([
        ("bakubus_official_alerts", bus_alerts),
        ("bakumetro_official_alerts", metro_alerts),
    ])
    return {
        "alerts": [_alert_to_dict(a) for a in merged],
        "priority_order": get_alert_priority_order(),
        "source_note": "Official BakuBus and Baku Metro pages first; not operator GTFS Realtime.",
    }


@router.get(
    "/transit/predicted-arrivals",
    summary="Predicted arrivals",
    description="Stop-level predicted arrivals where available. Public-web observed or licensed; never fake.",
)
def get_predicted_arrivals(stop_url: str = Query(None, description="Optional Yandex stop page URL")):
    from transit_ingestion.providers.yandex_transport_observed import (
        fetch_yandex_stop_page,
        normalize_yandex_stop_observations,
    )

    page = fetch_yandex_stop_page(stop_url=stop_url, timeout=10.0)
    arrivals, statuses, _ = normalize_yandex_stop_observations(page, stop_id="yandex_observed_stop")
    return {
        "predicted_arrivals": [
            {
                "prediction_id": a.prediction_id,
                "stop_id": a.stop_id,
                "route_id": a.route_id,
                "predicted_at": a.predicted_at.isoformat() if a.predicted_at else None,
                "observed_at": a.observed_at.isoformat() if a.observed_at else None,
                "source_provider": a.source_provider,
                "source_status": a.source_status,
                "confidence": a.confidence,
            }
            for a in arrivals
        ],
        "stop_statuses": [
            {
                "stop_id": s.stop_id,
                "status": s.status,
                "source_provider": s.source_provider,
                "source_status": s.source_status,
            }
            for s in statuses
        ],
        "source_note": "Public web observed from Yandex; not official operator feed.",
    }


@router.get(
    "/transit/realtime-observations",
    summary="Realtime observations",
    description="Route and stop observations from public-web sources. Truthful source_status.",
)
def get_realtime_observations():
    from transit_ingestion.providers.yandex_transport_observed import (
        fetch_yandex_stop_page,
        normalize_yandex_stop_observations,
    )
    from transit_ingestion.providers.yandex_metro_operational import (
        fetch_yandex_metro_page,
        normalize_yandex_metro_operational,
    )

    page = fetch_yandex_stop_page(timeout=8.0)
    _, statuses, route_obs = normalize_yandex_stop_observations(page)
    metro_page = fetch_yandex_metro_page(timeout=8.0)
    notices, constraints = normalize_yandex_metro_operational(metro_page)
    return {
        "stop_statuses": [
            {
                "stop_id": s.stop_id,
                "route_id": s.route_id,
                "status": s.status,
                "observed_at": s.observed_at.isoformat() if s.observed_at else None,
                "source_provider": s.source_provider,
                "source_family": s.source_family,
                "source_status": s.source_status,
                "source_url": s.source_url,
                "confidence": s.confidence,
                "validation_note": s.validation_note,
            }
            for s in statuses
        ],
        "route_observations": [
            {
                "route_id": o.route_id,
                "operating": o.operating,
                "observed_at": o.observed_at.isoformat() if o.observed_at else None,
                "source_provider": o.source_provider,
                "source_family": o.source_family,
                "source_status": o.source_status,
                "source_url": o.source_url,
                "confidence": o.confidence,
                "validation_note": o.validation_note,
            }
            for o in route_obs
        ],
        "metro_notices": [
            {
                "notice_id": n.notice_id,
                "station_id": n.station_id,
                "notice_type": n.notice_type,
                "description": n.description,
                "effective_start": n.effective_start.isoformat() if n.effective_start else None,
                "effective_end": n.effective_end.isoformat() if n.effective_end else None,
                "observed_at": n.observed_at.isoformat() if n.observed_at else None,
                "source_provider": n.source_provider,
                "source_family": n.source_family,
                "source_status": n.source_status,
                "source_url": n.source_url,
                "confidence": n.confidence,
                "validation_note": n.validation_note,
            }
            for n in notices
        ],
        "metro_constraints": [
            {
                "constraint_id": c.constraint_id,
                "from_station_id": c.from_station_id,
                "to_station_id": c.to_station_id,
                "constraint_type": c.constraint_type,
                "route_time_impact_seconds": c.route_time_impact_seconds,
                "observed_at": c.observed_at.isoformat() if c.observed_at else None,
                "source_provider": c.source_provider,
                "source_family": c.source_family,
                "source_status": c.source_status,
                "source_url": c.source_url,
                "confidence": c.confidence,
                "validation_note": c.validation_note,
            }
            for c in constraints
        ],
        "source_note": "Public web observed; not official operator GTFS Realtime.",
    }


@router.get(
    "/transit/provider-priority",
    summary="Provider priority policy",
    description="Source priority order for alerts, predicted arrivals, route planning.",
)
def get_provider_priority():
    from transit_ingestion.provenance.priority import (
        get_alert_priority_order,
        get_predicted_arrival_priority_order,
        get_route_planning_priority_order,
    )
    return {
        "alerts": get_alert_priority_order(),
        "predicted_arrivals": get_predicted_arrival_priority_order(),
        "route_planning": get_route_planning_priority_order(),
    }


@router.get(
    "/transit/source-status",
    summary="Source status by provider",
    description="Truthful status: official, public-web observed, licensed, unavailable.",
)
def get_source_status():
    from transit_ingestion.providers.yandex_traffic_context import get_traffic_context_status
    from transit_ingestion.providers.twogis_public_transport import get_twogis_status
    from transit_ingestion.providers.moovit_partner import get_moovit_status

    return {
        "providers": [
            {"provider_id": "bakubus_official_alerts", "source_family": "official_website", "source_status": "official_alerts_only"},
            {"provider_id": "bakumetro_official_alerts", "source_family": "official_website", "source_status": "official_alerts_only"},
            {"provider_id": "yandex_transport_observed", "source_family": "public_web", "source_status": "public_web_observed"},
            {"provider_id": "yandex_metro_operational", "source_family": "public_web", "source_status": "public_web_operational_context"},
            {"provider_id": "yandex_traffic_context", "source_family": "public_web_or_licensed", "source_status": get_traffic_context_status()},
            {"provider_id": "twogis_public_transport", "source_family": "licensed_api", "source_status": "licensed_partner", "configured": get_twogis_status() == "configured"},
            {"provider_id": "moovit_partner", "source_family": "licensed_api", "source_status": "partner_required", "configured": get_moovit_status() == "available"},
        ],
        "note": "Official and public-web sources are not operator GTFS Realtime.",
    }

"""
Alerts API.

This is the cross-domain alerts surface. It currently exposes transit-related alerts only.
It does not claim GTFS Realtime support when only observed web sources exist.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from iridium_schemas.transit import Alert

router = APIRouter()


def _fetch_transit_alerts() -> list[Alert]:
    from transit_ingestion.providers.bakubus_official_alerts import fetch_bakubus_alerts
    from transit_ingestion.providers.bakumetro_official_alerts import fetch_metro_alerts
    from transit_ingestion.provenance.priority import merge_alerts_by_priority

    bus_alerts = fetch_bakubus_alerts(timeout=15.0)
    metro_alerts = fetch_metro_alerts(timeout=15.0)
    merged = merge_alerts_by_priority(
        [
            ("bakubus_official_alerts", bus_alerts),
            ("bakumetro_official_alerts", metro_alerts),
        ]
    )
    return list(merged)


@router.get(
    "/alerts",
    summary="Operational alerts",
    description="Operational alerts from official and observed sources. Truthful source_status metadata.",
)
def list_alerts(
    provider: str | None = Query(None, description="Optional provider filter"),
    affected_mode: str | None = Query(None, description="Optional mode filter"),
) -> dict:
    alerts = _fetch_transit_alerts()
    if provider:
        alerts = [a for a in alerts if a.provider == provider or a.source_provider == provider]
    if affected_mode:
        alerts = [a for a in alerts if (a.affected_mode or "").lower() == affected_mode.lower()]
    return {
        "alerts": [a.model_dump(mode="json") for a in alerts],
        "note": "Transit alerts are from official websites or public-web observed sources. Not operator GTFS Realtime.",
    }


@router.get(
    "/alerts/{alert_id}",
    summary="Alert by ID",
    description="Fetch a specific alert by alert_id.",
)
def get_alert(alert_id: str) -> dict:
    alerts = _fetch_transit_alerts()
    for a in alerts:
        if a.alert_id == alert_id:
            return {"alert": a.model_dump(mode="json")}
    raise HTTPException(status_code=404, detail={"error": {"code": "not_found", "message": "Alert not found", "details": None}})


"""
Normalize AYNA getBusById (and getBusList) responses into canonical transit schema.
Uses actual fields: route number, firstPoint, lastPoint, tariff, durationMinuts, stops, flowCoordinates.
Deterministic IDs. source_family=public_api, source_status=public_undocumented.
"""

from datetime import datetime, timezone
from typing import Any, Optional

from iridium_schemas.transit import (
    TransitAgency,
    TransitRoute,
    TransitRouteVariant,
    TransitStop,
    TransitStopSequenceEntry,
    TransitShapePoint,
    TransitFarePolicy,
    SourceFamily,
    SourceStatus,
)

PROVIDER_ID = "bakubus_ayna"
SOURCE_FAMILY = SourceFamily.PUBLIC_API.value
SOURCE_STATUS = SourceStatus.PUBLIC_UNDOCUMENTED.value


def _ts() -> datetime:
    return datetime.now(timezone.utc)


def _safe_str(v: Any) -> str:
    if v is None:
        return ""
    return str(v).strip()


def _safe_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def normalize_bakubus_route(
    raw: Any,
    fetched_at: Optional[datetime] = None,
) -> tuple[
    Optional[TransitAgency],
    Optional[TransitRoute],
    Optional[TransitRouteVariant],
    list[TransitStop],
    list[TransitStopSequenceEntry],
    list[TransitShapePoint],
    Optional[TransitFarePolicy],
]:
    """
    Normalize a single getBusById response to canonical entities.
    Returns (agency, route, variant, stops, stop_sequence, shape_points, fare_policy).
    If raw is None or invalid, returns (None, None, None, [], [], [], None).
    """
    if raw is None or not isinstance(raw, dict):
        return (None, None, None, [], [], [], None)

    t = fetched_at or _ts()
    carrier = _safe_str(raw.get("carrier")) or "BakuBus"
    number = _safe_str(raw.get("number"))
    route_id_raw = raw.get("id") or raw.get("busId") or number
    route_id = f"bakubus_{_safe_str(route_id_raw)}"
    variant_id = f"{route_id}_variant"

    agency = TransitAgency(
        agency_id="bakubus",
        name=carrier or "BakuBus",
        url="https://bakubus.az",
        timezone="Asia/Baku",
        source_provider=PROVIDER_ID,
        source_family=SOURCE_FAMILY,
        source_status=SOURCE_STATUS,
        fetched_at=t,
    )

    route = TransitRoute(
        route_id=route_id,
        agency_id="bakubus",
        short_name=number or None,
        long_name=None,
        route_type="3",
        source_provider=PROVIDER_ID,
        source_family=SOURCE_FAMILY,
        source_status=SOURCE_STATUS,
        fetched_at=t,
    )

    first_point = _safe_str(raw.get("firstPoint"))
    last_point = _safe_str(raw.get("lastPoint"))
    variant = TransitRouteVariant(
        variant_id=variant_id,
        route_id=route_id,
        first_point=first_point or None,
        last_point=last_point or None,
        source_provider=PROVIDER_ID,
        source_family=SOURCE_FAMILY,
        source_status=SOURCE_STATUS,
        fetched_at=t,
    )

    stops_in: list[Any] = raw.get("stops") if isinstance(raw.get("stops"), list) else []
    stops: list[TransitStop] = []
    stop_sequence: list[TransitStopSequenceEntry] = []
    for i, s in enumerate(stops_in):
        if not isinstance(s, dict):
            continue
        sid = _safe_str(s.get("id") or s.get("name") or s.get("stopId")) or f"stop_{i}"
        stop_id = f"bakubus_{route_id}_{sid}"
        lat = _safe_float(s.get("lat") or s.get("latitude"))
        lon = _safe_float(s.get("lon") or s.get("longitude"))
        name = _safe_str(s.get("name") or s.get("title")) or None
        stops.append(
            TransitStop(
                stop_id=stop_id,
                name=name if name else None,
                lat=lat,
                lon=lon,
                stop_sequence=i + 1,
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                fetched_at=t,
            )
        )
        stop_sequence.append(
            TransitStopSequenceEntry(
                variant_id=variant_id,
                stop_id=stop_id,
                sequence=i + 1,
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                fetched_at=t,
            )
        )

    shape_points: list[TransitShapePoint] = []
    flow = raw.get("flowCoordinates")
    if isinstance(flow, list):
        shape_id = f"{variant_id}_shape"
        for j, pt in enumerate(flow):
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                lat = _safe_float(pt[0])
                lon = _safe_float(pt[1])
            elif isinstance(pt, dict):
                lat = _safe_float(pt.get("lat") or pt.get("latitude"))
                lon = _safe_float(pt.get("lon") or pt.get("longitude"))
            else:
                continue
            if lat is not None and lon is not None:
                shape_points.append(
                    TransitShapePoint(
                        shape_id=shape_id,
                        sequence=j + 1,
                        lat=lat,
                        lon=lon,
                        source_provider=PROVIDER_ID,
                        source_family=SOURCE_FAMILY,
                        source_status=SOURCE_STATUS,
                        fetched_at=t,
                    )
                )

    fare_policy: Optional[TransitFarePolicy] = None
    tariff = raw.get("tariff")
    if tariff is not None:
        price = _safe_float(tariff) if isinstance(tariff, (int, float, str)) else None
        if price is not None or isinstance(tariff, str):
            fare_policy = TransitFarePolicy(
                fare_id=f"bakubus_{route_id}_fare",
                agency_id="bakubus",
                price=price,
                currency="AZN",
                description="BakıKART fare; no cash. Source: AYNA API.",
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                fetched_at=t,
            )

    return (agency, route, variant, stops, stop_sequence, shape_points, fare_policy)


def normalize_bus_list(raw_list: Any, fetched_at: Optional[datetime] = None) -> list[dict]:
    """
    Normalize getBusList response to a list of {id, number?, ...} for downstream getBusById.
    Does not invent IDs; uses only present fields.
    """
    if raw_list is None:
        return []
    if isinstance(raw_list, list):
        out = []
        for item in raw_list:
            if isinstance(item, dict):
                out.append({
                    "id": item.get("id") or item.get("busId") or item.get("number"),
                    "number": item.get("number"),
                    "raw": item,
                })
            elif item is not None:
                out.append({"id": str(item), "number": None, "raw": item})
        return out
    if isinstance(raw_list, dict) and "data" in raw_list:
        return normalize_bus_list(raw_list["data"], fetched_at)
    return []

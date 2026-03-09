"""
Merge BakuBus and Baku Metro normalized data into a single transit snapshot.
Deterministic ordering; no duplication of agency/route by id.
"""

from datetime import datetime, timezone
from typing import Optional

from iridium_schemas.transit import (
    TransitAgency,
    TransitRoute,
    TransitRouteVariant,
    TransitStop,
    TransitStopSequenceEntry,
    TransitShapePoint,
    TransitInterchange,
    TransitFarePolicy,
    TransitServiceWindow,
    TransitSnapshotMetadata,
)


def build_unified_transit_snapshot(
    bakubus_routes: Optional[list[dict]] = None,
    bakumetro_network: Optional[dict] = None,
    fetched_at: Optional[datetime] = None,
) -> dict:
    """
    Build one snapshot with agencies, routes, variants, stops, stop_sequences, shapes,
    interchanges, fare and service from both providers. Each list is deduplicated by id.
    """
    from transit_ingestion.providers.bakumetro_official.static_network import (
        build_static_metro_network,
    )

    t = fetched_at or datetime.now(timezone.utc)
    agencies: list[TransitAgency] = []
    routes: list[TransitRoute] = []
    variants: list[TransitRouteVariant] = []
    stops: list[TransitStop] = []
    stop_sequences: list[TransitStopSequenceEntry] = []
    shapes: list[TransitShapePoint] = []
    interchanges: list[TransitInterchange] = []
    fare_policies: list[TransitFarePolicy] = []
    service_windows: list[TransitServiceWindow] = []

    seen_agency: set[str] = set()
    seen_route: set[str] = set()
    seen_variant: set[str] = set()
    seen_stop: set[str] = set()

    if bakubus_routes:  # pragma: no cover
        for item in bakubus_routes:
            ag = item.get("agency")
            if ag and ag.agency_id not in seen_agency:
                seen_agency.add(ag.agency_id)
                agencies.append(ag)
            r = item.get("route")
            if r and r.route_id not in seen_route:
                seen_route.add(r.route_id)
                routes.append(r)
            v = item.get("variant")
            if v and v.variant_id not in seen_variant:
                seen_variant.add(v.variant_id)
                variants.append(v)
            for s in item.get("stops") or []:
                if s.stop_id not in seen_stop:
                    seen_stop.add(s.stop_id)
                    stops.append(s)
            stop_sequences.extend(item.get("stop_sequence") or [])
            shapes.extend(item.get("shape_points") or [])
            fp = item.get("fare_policy")
            if fp:
                fare_policies.append(fp)

    metro = bakumetro_network or build_static_metro_network(t)
    if metro.get("agency") and metro["agency"].agency_id not in seen_agency:
        agencies.append(metro["agency"])
    for r in metro.get("routes") or []:
        if r.route_id not in seen_route:
            seen_route.add(r.route_id)
            routes.append(r)
    for s in metro.get("stops") or []:
        if s.stop_id not in seen_stop:
            seen_stop.add(s.stop_id)
            stops.append(s)
    interchanges = metro.get("interchanges") or []
    if metro.get("fare_policy"):
        fare_policies.append(metro["fare_policy"])
    if metro.get("service_window"):
        service_windows.append(metro["service_window"])

    return {
        "agencies": agencies,
        "routes": routes,
        "variants": variants,
        "stops": stops,
        "stop_sequences": stop_sequences,
        "shapes": shapes,
        "interchanges": interchanges,
        "fare_policies": fare_policies,
        "service_windows": service_windows,
        "metadata": {
            "fetched_at": t.isoformat(),
            "providers": ["bakubus_ayna", "bakumetro_official"],
            "timetable_available": False,
        },
    }

"""
Readiness report: static stop discovery, route visualization, transfer graph, timetable routing.
Honest: timetable_routing only true when exact stop_times are available.
"""

from iridium_schemas.transit import TransitReadinessReport


def compute_readiness_report(snapshot: dict) -> TransitReadinessReport:
    """
    Answer: Can this data support static stop discovery, route visualization,
    transfer graph construction, timetable routing? What is missing for OTP-grade deployment?
    """
    stops = snapshot.get("stops") or []
    routes = snapshot.get("routes") or []
    shapes = snapshot.get("shapes") or []
    interchanges = snapshot.get("interchanges") or []
    has_stop_times = bool(snapshot.get("stop_times") or snapshot.get("trips"))

    static_stop_discovery = len(stops) > 0
    route_visualization = len(routes) > 0 and (len(shapes) > 0 or len(stops) > 0)
    transfer_graph = len(interchanges) > 0 or len(stops) > 1
    timetable_routing = has_stop_times

    missing: list[str] = []
    if not has_stop_times:
        missing.append("Exact stop_times/trips not available; timetable routing not supported.")
    stops_without_coords = sum(1 for s in stops if getattr(s, "lat", None) is None)
    if stops_without_coords:
        missing.append(
            f"{stops_without_coords} stops lack coordinates; OSM resolution or manual input required."
        )
    missing.append("GTFS Realtime (trip updates, vehicle positions) not available.")

    capabilities = {
        "bakubus_ayna": ["routes", "stops", "shapes", "fare_basic"],
        "bakumetro_official": ["routes", "stops", "interchanges", "service_window", "fare_basic"],
    }
    return TransitReadinessReport(
        static_stop_discovery=static_stop_discovery,
        route_visualization=route_visualization,
        transfer_graph=transfer_graph,
        timetable_routing=timetable_routing,
        missing_for_otp=missing,
        provider_capabilities=capabilities,
    )

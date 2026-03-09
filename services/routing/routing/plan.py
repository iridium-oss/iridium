"""
Multimodal route planning baseline. Weighted shortest path with time/cost/carbon.
Uses digital twin graph; origin/destination snapped to nearest nodes for demo.
"""

from datetime import datetime, timezone

from iridium_schemas.routing import (
    RouteRequest,
    RouteResponse,
    RouteAlternative,
    RouteSegment,
)
from digital_twin.service import get_snapshot


def _weight(optimize: str, duration_min: float, cost: float, carbon_kg: float) -> float:
    if optimize == "cost":
        return duration_min * 0.2 + cost * 2.0 + (carbon_kg or 0) * 0.1
    if optimize == "carbon":
        return duration_min * 0.1 + (cost or 0) * 0.2 + (carbon_kg or 0) * 5.0
    return duration_min * 1.0 + (cost or 0) * 0.1 + (carbon_kg or 0) * 0.5


def plan_routes(req: RouteRequest) -> RouteResponse:
    """Compute route alternatives. Baseline: use twin graph and weighted path."""
    snapshot = get_snapshot()
    if not snapshot.nodes or not snapshot.edges:
        return RouteResponse(alternatives=[], note="No network loaded.")
    # Snap origin/dest to nearest nodes (by lat/lon distance)
    def dist(n: object, lat: float, lon: float) -> float:
        if not hasattr(n, "lat") or n.lat is None or n.lon is None:
            return 1e9
        return (n.lat - lat) ** 2 + (n.lon - lon) ** 2
    nodes = snapshot.nodes
    by_dist_orig = sorted(nodes, key=lambda n: dist(n, req.origin_lat, req.origin_lon))
    by_dist_dest = sorted(nodes, key=lambda n: dist(n, req.destination_lat, req.destination_lon))
    start_id = by_dist_orig[0].node_id if by_dist_orig else "n1"
    end_id = by_dist_dest[0].node_id if by_dist_dest else "n5"
    # Build simple path: filter edges by allowed modes, then BFS/dijkstra placeholder
    allowed = set(req.modes) if req.modes else {"walking", "bus", "metro", "minibus", "cycling", "road"}
    edges = [e for e in snapshot.edges if e.mode in allowed]
    # Shortest path by travel_time_min (simplified: first path found)
    from collections import defaultdict
    adj: dict[str, list[tuple[str, float, float, float, str]]] = defaultdict(list)
    for e in edges:
        adj[e.from_node].append((e.to_node, e.travel_time_min or 5.0, e.cost or 0, e.carbon_kg or 0, e.mode))
    best_weight = 1e9
    best_path: list[tuple[str, float, float, float, str]] = []
    def dfs(node: str, path: list[tuple[str, float, float, float, str]], visited: set[str]) -> None:
        nonlocal best_weight, best_path
        if node == end_id:
            d = sum(p[1] for p in path)
            c = sum(p[2] for p in path)
            carb = sum(p[3] for p in path)
            w = _weight(req.optimize, d, c, carb)
            if w < best_weight:
                best_weight = w
                best_path = list(path)
            return
        for to_node, dur, cost, carb, mode in adj[node]:
            if to_node in visited:
                continue
            visited.add(to_node)
            path.append((to_node, dur, cost, carb, mode))
            dfs(to_node, path, visited)
            path.pop()
            visited.discard(to_node)
    dfs(start_id, [], {start_id})
    if not best_path:
        # Fallback: single walking segment as placeholder
        total_d = 15.0
        total_c = 0.0
        total_carb = 0.0
        segs = [
            RouteSegment(
                mode="walking",
                duration_min=total_d,
                cost=total_c,
                carbon_kg=total_carb,
                description="Baseline placeholder route",
            )
        ]
    else:
        segs = [
            RouteSegment(
                mode=mode,
                to_node_id=to_node,
                duration_min=dur,
                cost=cost,
                carbon_kg=carb,
            )
            for to_node, dur, cost, carb, mode in best_path
        ]
        total_d = sum(s.duration_min for s in segs)
        total_c = sum(s.cost or 0 for s in segs)
        total_carb = sum(s.carbon_kg or 0 for s in segs)
    alt = RouteAlternative(
        segments=segs,
        total_duration_min=total_d,
        total_cost=total_c,
        total_carbon_kg=total_carb,
        transfer_count=max(0, len(segs) - 1),
        score_time=total_d,
        score_cost=total_c,
        score_carbon=total_carb,
    )
    return RouteResponse(
        alternatives=[alt],
        requested_at=datetime.now(timezone.utc),
        note="Baseline optimizer; full journey planner planned.",
    )

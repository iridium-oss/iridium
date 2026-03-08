"""
Routing endpoint.
"""

from fastapi import APIRouter

from iridium_schemas.routing import RouteRequest, RouteResponse
from routing.plan import plan_routes

router = APIRouter()


@router.post("/routing/plan", response_model=RouteResponse, summary="Plan multimodal route")
def post_routing_plan(body: RouteRequest) -> RouteResponse:
    """Compute one or more route alternatives. Baseline optimizer."""
    return plan_routes(body)

"""
Routing API request and response schemas.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    """POST /api/v1/routing/plan body."""

    origin_lat: float = Field(..., ge=-90, le=90)
    origin_lon: float = Field(..., ge=-180, le=180)
    destination_lat: float = Field(..., ge=-90, le=90)
    destination_lon: float = Field(..., ge=-180, le=180)
    modes: list[str] = Field(
        default_factory=lambda: ["walking", "bus", "metro", "minibus", "cycling"],
        description="Preferred modes",
    )
    max_transfers: int | None = Field(None, ge=0, le=10)
    optimize: str = Field("time", description="time | cost | carbon")
    departure_time: datetime | None = None


class RouteSegment(BaseModel):
    """Single leg of a route."""

    mode: str
    from_node_id: str | None = None
    to_node_id: str | None = None
    duration_min: float = Field(..., ge=0)
    cost: float | None = Field(None, ge=0)
    carbon_kg: float | None = Field(None, ge=0)
    description: str | None = None


class RouteAlternative(BaseModel):
    """One route alternative with scoring fields."""

    segments: list[RouteSegment] = Field(default_factory=list)
    total_duration_min: float = Field(..., ge=0)
    total_cost: float | None = Field(None, ge=0)
    total_carbon_kg: float | None = Field(None, ge=0)
    transfer_count: int = Field(0, ge=0)
    score_time: float | None = None
    score_cost: float | None = None
    score_carbon: float | None = None


class RouteResponse(BaseModel):
    """Response for POST /api/v1/routing/plan."""

    alternatives: list[RouteAlternative] = Field(default_factory=list)
    requested_at: datetime = Field(default_factory=datetime.utcnow)
    note: str | None = Field(None, description="e.g. baseline optimizer")
    model_type: str | None = Field(
        None,
        description="deterministic_baseline | rule_baseline",
    )
    model_maturity: str | None = Field(
        None,
        description="production_baseline | experimental | inactive",
    )
    data_status: str | None = Field(
        None,
        description="live | unavailable | configuration_required when network not loaded.",
    )
    fallback_used: bool = Field(
        False,
        description="True if no path found and placeholder or fallback route was returned.",
    )

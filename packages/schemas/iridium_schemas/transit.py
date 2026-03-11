"""
Canonical transit schema for normalized BakuBus and Baku Metro data.
Every record includes source_provider, source_family, source_status, fetched_at.
No fabricated feeds or timetables.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SourceFamily(str, Enum):
    OFFICIAL_MACHINE_READABLE = "official_machine_readable"
    OFFICIAL_WEBSITE = "official_website"
    PUBLIC_API = "public_api"
    PUBLIC_UNDOCUMENTED = "public_undocumented"
    PUBLIC_WEB = "public_web"
    LICENSED_API = "licensed_api"
    PERMISSION_REQUIRED = "permission_required"
    UNAVAILABLE = "unavailable"


class SourceStatus(str, Enum):
    OFFICIAL_MACHINE_READABLE = "official_machine_readable"
    OFFICIAL_WEBSITE = "official_website"
    OFFICIAL_ALERTS_ONLY = "official_alerts_only"
    STATIC_SCHEDULE_ONLY = "static_schedule_only"
    PUBLIC_API = "public_api"
    PUBLIC_UNDOCUMENTED = "public_undocumented"
    PUBLIC_WEB_OBSERVED = "public_web_observed"
    PUBLIC_WEB_OPERATIONAL_CONTEXT = "public_web_operational_context"
    LICENSED_PARTNER = "licensed_partner"
    PARTNER_REQUIRED = "partner_required"
    PERMISSION_REQUIRED = "permission_required"
    UNAVAILABLE = "unavailable"


class TransitSnapshotMetadata(BaseModel):
    """Metadata for a transit snapshot: provenance and scope."""

    source_provider: str = Field(..., description="e.g. bakubus_ayna, bakumetro_official")
    source_family: str = Field(
        ..., description="official_website | public_api | public_undocumented | etc."
    )
    source_status: str = Field(..., description="static_schedule_only | public_undocumented | etc.")
    fetched_at: datetime | None = None
    effective_date: str | None = None
    confidence: str | None = None
    validation_note: str | None = None


class TransitAgency(BaseModel):
    """Transit operator/agency."""

    agency_id: str
    name: str
    url: str | None = None
    timezone: str | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None


class TransitRoute(BaseModel):
    """Route (e.g. bus route number or metro line)."""

    route_id: str
    agency_id: str
    short_name: str | None = None
    long_name: str | None = None
    route_type: str | None = Field(None, description="3=bus, 1=metro, etc.")
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None


class TransitRouteVariant(BaseModel):
    """Directional variant of a route (e.g. A to B)."""

    variant_id: str
    route_id: str
    first_point: str | None = None
    last_point: str | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None


class TransitStop(BaseModel):
    """Stop or station."""

    stop_id: str
    name: str | None = None
    lat: float | None = Field(None, ge=-90, le=90)
    lon: float | None = Field(None, ge=-180, le=180)
    stop_sequence: int | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None
    osm_match_confidence: str | None = None


class TransitStopSequenceEntry(BaseModel):
    """Stop in sequence for a route variant."""

    variant_id: str
    stop_id: str
    sequence: int
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None


class TransitShapePoint(BaseModel):
    """Point on route shape (geometry)."""

    shape_id: str
    sequence: int
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None


class TransitInterchange(BaseModel):
    """Transfer / interchange between stations or stops."""

    from_stop_id: str
    to_stop_id: str
    from_route_id: str | None = None
    to_route_id: str | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None


class TransitFarePolicy(BaseModel):
    """Basic fare rule (no fabricated prices)."""

    fare_id: str | None = None
    agency_id: str
    price: float | None = None
    currency: str | None = None
    description: str | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None


class TransitServiceWindow(BaseModel):
    """Operating hours / service window."""

    agency_id: str
    start_time: str | None = None
    end_time: str | None = None
    description: str | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: datetime | None = None


class TransitReadinessReport(BaseModel):
    """Readiness for static discovery, visualization, transfer graph, timetable routing."""

    static_stop_discovery: bool = False
    route_visualization: bool = False
    transfer_graph: bool = False
    timetable_routing: bool = False
    missing_for_otp: list[str] = Field(default_factory=list)
    provider_capabilities: dict = Field(default_factory=dict)


# Realtime and supplementary data (no fabricated feeds).


class Alert(BaseModel):
    """Service alert from official or observed source. Not operator GTFS Realtime."""

    alert_id: str
    title: str | None = None
    published_at: datetime | None = None
    provider: str = ""
    affected_mode: str | None = None
    affected_route_id: str | None = None
    affected_station_id: str | None = None
    alert_category: str | None = None
    severity: str | None = None
    effective_start: datetime | None = None
    effective_end: datetime | None = None
    source_url: str | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    observed_at: datetime | None = None
    fetched_at: datetime | None = None
    confidence: str | None = None
    validation_note: str | None = None


class PredictedArrival(BaseModel):
    """Stop-level predicted arrival. Source may be official feed or public-web observed."""

    prediction_id: str
    stop_id: str
    route_id: str | None = None
    trip_id: str | None = None
    predicted_at: datetime | None = None
    observed_at: datetime | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: str | None = None
    scrape_method: str | None = None
    parser_version: str | None = None
    confidence: str | None = None
    validation_note: str | None = None


class StopRealtimeStatus(BaseModel):
    """Observed realtime status at a stop (e.g. operating, not operating)."""

    stop_id: str
    route_id: str | None = None
    status: str | None = None
    observed_at: datetime | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: str | None = None
    confidence: str | None = None
    validation_note: str | None = None


class RouteRealtimeObservation(BaseModel):
    """Route-level observation (e.g. headway, visible identifiers). Public-web observed."""

    route_id: str | None = None
    external_route_ref: str | None = None
    headway_seconds: int | None = None
    operating: bool | None = None
    observed_at: datetime | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: str | None = None
    confidence: str | None = None
    validation_note: str | None = None


class MetroOperationalNotice(BaseModel):
    """Metro operational modifier (e.g. closed station, entrance restriction)."""

    notice_id: str
    station_id: str | None = None
    notice_type: str | None = None
    description: str | None = None
    effective_start: datetime | None = None
    effective_end: datetime | None = None
    observed_at: datetime | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: str | None = None
    confidence: str | None = None
    validation_note: str | None = None


class MetroRoutingConstraint(BaseModel):
    """Constraint affecting metro route planning (closed segment, time impact)."""

    constraint_id: str
    from_station_id: str | None = None
    to_station_id: str | None = None
    constraint_type: str | None = None
    route_time_impact_seconds: int | None = None
    observed_at: datetime | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: str | None = None
    confidence: str | None = None
    validation_note: str | None = None


class SegmentCongestionLevel(BaseModel):
    """Road segment congestion level. Web observed or licensed API."""

    segment_id: str | None = None
    level: str | None = None
    observed_at: datetime | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    confidence: str | None = None
    validation_note: str | None = None


class RoadTrafficContext(BaseModel):
    """Road traffic context for Baku. Not operator feed."""

    context_id: str
    observed_at: datetime | None = None
    segments: list[SegmentCongestionLevel] = Field(default_factory=list)
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: str | None = None
    confidence: str | None = None
    validation_note: str | None = None


class TravelTimeContext(BaseModel):
    """Travel time context from routing/traffic source."""

    segment_id: str | None = None
    duration_seconds: int | None = None
    observed_at: datetime | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    confidence: str | None = None
    validation_note: str | None = None


class TransitPartnerRouteResult(BaseModel):
    """Route planning result from licensed partner (2GIS, Moovit, Yandex). Not operator ground truth."""

    result_id: str
    total_duration_seconds: int | None = None
    transfer_count: int | None = None
    route_variants: list[str] = Field(default_factory=list)
    schedules_returned: bool = False
    observed_at: datetime | None = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: str | None = None
    confidence: str | None = None
    validation_note: str | None = None

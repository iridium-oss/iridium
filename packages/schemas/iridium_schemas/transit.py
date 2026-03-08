"""
Canonical transit schema for normalized BakuBus and Baku Metro data.
Every record includes source_provider, source_family, source_status, fetched_at.
No fabricated feeds or timetables.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

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
    source_family: str = Field(..., description="official_website | public_api | public_undocumented | etc.")
    source_status: str = Field(..., description="static_schedule_only | public_undocumented | etc.")
    fetched_at: Optional[datetime] = None
    effective_date: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class TransitAgency(BaseModel):
    """Transit operator/agency."""

    agency_id: str
    name: str
    url: Optional[str] = None
    timezone: Optional[str] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None


class TransitRoute(BaseModel):
    """Route (e.g. bus route number or metro line)."""

    route_id: str
    agency_id: str
    short_name: Optional[str] = None
    long_name: Optional[str] = None
    route_type: Optional[str] = Field(None, description="3=bus, 1=metro, etc.")
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None


class TransitRouteVariant(BaseModel):
    """Directional variant of a route (e.g. A to B)."""

    variant_id: str
    route_id: str
    first_point: Optional[str] = None
    last_point: Optional[str] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None


class TransitStop(BaseModel):
    """Stop or station."""

    stop_id: str
    name: Optional[str] = None
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lon: Optional[float] = Field(None, ge=-180, le=180)
    stop_sequence: Optional[int] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None
    osm_match_confidence: Optional[str] = None


class TransitStopSequenceEntry(BaseModel):
    """Stop in sequence for a route variant."""

    variant_id: str
    stop_id: str
    sequence: int
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None


class TransitShapePoint(BaseModel):
    """Point on route shape (geometry)."""

    shape_id: str
    sequence: int
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None


class TransitInterchange(BaseModel):
    """Transfer / interchange between stations or stops."""

    from_stop_id: str
    to_stop_id: str
    from_route_id: Optional[str] = None
    to_route_id: Optional[str] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None


class TransitFarePolicy(BaseModel):
    """Basic fare rule (no fabricated prices)."""

    fare_id: Optional[str] = None
    agency_id: str
    price: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None


class TransitServiceWindow(BaseModel):
    """Operating hours / service window."""

    agency_id: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    description: Optional[str] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    fetched_at: Optional[datetime] = None


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
    title: Optional[str] = None
    published_at: Optional[datetime] = None
    provider: str = ""
    affected_mode: Optional[str] = None
    affected_route_id: Optional[str] = None
    affected_station_id: Optional[str] = None
    alert_category: Optional[str] = None
    severity: Optional[str] = None
    effective_start: Optional[datetime] = None
    effective_end: Optional[datetime] = None
    source_url: Optional[str] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    observed_at: Optional[datetime] = None
    fetched_at: Optional[datetime] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class PredictedArrival(BaseModel):
    """Stop-level predicted arrival. Source may be official feed or public-web observed."""

    prediction_id: str
    stop_id: str
    route_id: Optional[str] = None
    trip_id: Optional[str] = None
    predicted_at: Optional[datetime] = None
    observed_at: Optional[datetime] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: Optional[str] = None
    scrape_method: Optional[str] = None
    parser_version: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class StopRealtimeStatus(BaseModel):
    """Observed realtime status at a stop (e.g. operating, not operating)."""

    stop_id: str
    route_id: Optional[str] = None
    status: Optional[str] = None
    observed_at: Optional[datetime] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class RouteRealtimeObservation(BaseModel):
    """Route-level observation (e.g. headway, visible identifiers). Public-web observed."""

    route_id: Optional[str] = None
    external_route_ref: Optional[str] = None
    headway_seconds: Optional[int] = None
    operating: Optional[bool] = None
    observed_at: Optional[datetime] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class MetroOperationalNotice(BaseModel):
    """Metro operational modifier (e.g. closed station, entrance restriction)."""

    notice_id: str
    station_id: Optional[str] = None
    notice_type: Optional[str] = None
    description: Optional[str] = None
    effective_start: Optional[datetime] = None
    effective_end: Optional[datetime] = None
    observed_at: Optional[datetime] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class MetroRoutingConstraint(BaseModel):
    """Constraint affecting metro route planning (closed segment, time impact)."""

    constraint_id: str
    from_station_id: Optional[str] = None
    to_station_id: Optional[str] = None
    constraint_type: Optional[str] = None
    route_time_impact_seconds: Optional[int] = None
    observed_at: Optional[datetime] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class SegmentCongestionLevel(BaseModel):
    """Road segment congestion level. Web observed or licensed API."""

    segment_id: Optional[str] = None
    level: Optional[str] = None
    observed_at: Optional[datetime] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class RoadTrafficContext(BaseModel):
    """Road traffic context for Baku. Not operator feed."""

    context_id: str
    observed_at: Optional[datetime] = None
    segments: list[SegmentCongestionLevel] = Field(default_factory=list)
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class TravelTimeContext(BaseModel):
    """Travel time context from routing/traffic source."""

    segment_id: Optional[str] = None
    duration_seconds: Optional[int] = None
    observed_at: Optional[datetime] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class TransitPartnerRouteResult(BaseModel):
    """Route planning result from licensed partner (2GIS, Moovit, Yandex). Not operator ground truth."""

    result_id: str
    total_duration_seconds: Optional[int] = None
    transfer_count: Optional[int] = None
    route_variants: list[str] = Field(default_factory=list)
    schedules_returned: bool = False
    observed_at: Optional[datetime] = None
    source_provider: str = ""
    source_family: str = ""
    source_status: str = ""
    source_url: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None

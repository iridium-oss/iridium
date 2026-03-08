"""
Ingestion event schemas: sensor, GNSS, weather, events, energy.
All data is non-personal; GNSS is assumed aggregated or anonymised at source.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SensorEvent(BaseModel):
    """Single road sensor observation (IoT)."""

    segment_id: str = Field(..., description="Road segment identifier")
    timestamp: datetime
    speed_kmh: Optional[float] = Field(None, ge=0, le=200)
    occupancy_pct: Optional[float] = Field(None, ge=0, le=100)
    flow_count: Optional[int] = Field(None, ge=0)
    source_id: Optional[str] = None


class GNSSPoint(BaseModel):
    """Aggregated or anonymised GNSS-derived point (no device identity)."""

    segment_id: Optional[str] = None
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    timestamp: datetime
    speed_kmh: Optional[float] = Field(None, ge=0, le=200)
    count: Optional[int] = Field(None, ge=0, description="Aggregate count if applicable")


class WeatherSnapshot(BaseModel):
    """Meteorological snapshot for a location or region."""

    timestamp: datetime
    region_id: str = Field(..., description="City or zone identifier")
    temp_c: Optional[float] = None
    precipitation_mm: Optional[float] = Field(None, ge=0)
    visibility_km: Optional[float] = Field(None, ge=0)
    condition: Optional[str] = None


class PublicEventRecord(BaseModel):
    """Public event from a calendar feed."""

    event_id: str
    start_time: datetime
    end_time: datetime
    venue_or_zone_id: str
    capacity: Optional[int] = Field(None, ge=0)
    event_type: Optional[str] = None


class EnergyGridSignal(BaseModel):
    """Optional energy grid signal (e.g. for future EV integration)."""

    zone_id: str
    timestamp: datetime
    price_per_kwh: Optional[float] = Field(None, ge=0)
    capacity_fraction: Optional[float] = Field(None, ge=0, le=1)


class IngestionEventBatch(BaseModel):
    """Batch of ingestion events for POST /api/v1/ingestion/events."""

    sensor_events: list[SensorEvent] = Field(default_factory=list)
    gnss_points: list[GNSSPoint] = Field(default_factory=list)
    weather: list[WeatherSnapshot] = Field(default_factory=list)
    public_events: list[PublicEventRecord] = Field(default_factory=list)
    energy_signals: list[EnergyGridSignal] = Field(default_factory=list)

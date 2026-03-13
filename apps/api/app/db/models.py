"""
Database models for IRIDIUM API persistence layer.

Models are intentionally minimal and additive. They focus on provenance-aware auditing
and storage of normalized transit, weather, snapshots, and operational records.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SourceProvider(Base):
    __tablename__ = "source_providers"

    provider_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    source_family: Mapped[str] = mapped_column(String, nullable=False)
    source_status: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class SourceFetchLog(Base):
    __tablename__ = "source_fetch_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    error_class: Mapped[str | None] = mapped_column(String, nullable=True)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class TransitRoute(Base):
    __tablename__ = "transit_routes"

    route_id: Mapped[str] = mapped_column(String, primary_key=True)
    agency_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    short_name: Mapped[str | None] = mapped_column(String, nullable=True)
    long_name: Mapped[str | None] = mapped_column(String, nullable=True)
    route_type: Mapped[str | None] = mapped_column(String, nullable=True)

    source_provider: Mapped[str] = mapped_column(String, nullable=False)
    source_family: Mapped[str] = mapped_column(String, nullable=False)
    source_status: Mapped[str] = mapped_column(String, nullable=False)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence: Mapped[str | None] = mapped_column(String, nullable=True)
    validation_note: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class TransitStop(Base):
    __tablename__ = "transit_stops"

    stop_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)

    source_provider: Mapped[str] = mapped_column(String, nullable=False)
    source_family: Mapped[str] = mapped_column(String, nullable=False)
    source_status: Mapped[str] = mapped_column(String, nullable=False)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence: Mapped[str | None] = mapped_column(String, nullable=True)
    validation_note: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class TransitRouteStop(Base):
    __tablename__ = "transit_route_stops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    route_id: Mapped[str] = mapped_column(
        String, ForeignKey("transit_routes.route_id"), nullable=False, index=True
    )
    stop_id: Mapped[str] = mapped_column(
        String, ForeignKey("transit_stops.stop_id"), nullable=False, index=True
    )
    stop_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    direction_id: Mapped[str | None] = mapped_column(String, nullable=True)
    variant_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class TransitRouteShape(Base):
    __tablename__ = "transit_route_shapes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    route_id: Mapped[str] = mapped_column(
        String, ForeignKey("transit_routes.route_id"), nullable=False, index=True
    )
    variant_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    geom_geojson: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    source_provider: Mapped[str] = mapped_column(String, nullable=False)
    source_family: Mapped[str] = mapped_column(String, nullable=False)
    source_status: Mapped[str] = mapped_column(String, nullable=False)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class OfficialAlert(Base):
    __tablename__ = "official_alerts"

    alert_id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    affected_mode: Mapped[str | None] = mapped_column(String, nullable=True)
    affected_route_id: Mapped[str | None] = mapped_column(String, nullable=True)
    affected_station_id: Mapped[str | None] = mapped_column(String, nullable=True)
    alert_category: Mapped[str | None] = mapped_column(String, nullable=True)
    severity: Mapped[str | None] = mapped_column(String, nullable=True)
    effective_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    source_provider: Mapped[str] = mapped_column(String, nullable=False)
    source_family: Mapped[str] = mapped_column(String, nullable=False)
    source_status: Mapped[str] = mapped_column(String, nullable=False)
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    confidence: Mapped[str | None] = mapped_column(String, nullable=True)
    validation_note: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class PublicWebObservation(Base):
    __tablename__ = "public_web_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    observation_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    subject_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence: Mapped[str | None] = mapped_column(String, nullable=True)
    validation_note: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    source_provider: Mapped[str] = mapped_column(String, nullable=False)
    source_family: Mapped[str] = mapped_column(String, nullable=False)
    source_status: Mapped[str] = mapped_column(String, nullable=False)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence: Mapped[str | None] = mapped_column(String, nullable=True)
    validation_note: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class DigitalTwinSnapshotRecord(Base):
    __tablename__ = "digital_twin_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    data_status: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    provenance: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class AnomalyRecord(Base):
    __tablename__ = "anomaly_records"

    anomaly_id: Mapped[str] = mapped_column(String, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String, nullable=False, index=True)
    segment_ids: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    zone_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    valid_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommended_response: Mapped[str | None] = mapped_column(Text, nullable=True)

    source_provider: Mapped[str] = mapped_column(String, nullable=False)
    source_family: Mapped[str] = mapped_column(String, nullable=False)
    source_status: Mapped[str] = mapped_column(String, nullable=False)
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence: Mapped[str | None] = mapped_column(String, nullable=True)
    validation_note: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )


class ForecastSnapshotRecord(Base):
    __tablename__ = "forecast_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    horizon_minutes: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    segment_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    model_version: Mapped[str | None] = mapped_column(String, nullable=True)

    source_provider: Mapped[str] = mapped_column(String, nullable=False)
    source_family: Mapped[str] = mapped_column(String, nullable=False)
    source_status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )

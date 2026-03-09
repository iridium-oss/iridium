"""backend core tables

Revision ID: 0002_backend_core_tables
Revises: 0001_initial_tables
Create Date: 2026-03-09
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_backend_core_tables"
down_revision = "0001_initial_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "transit_routes",
        sa.Column("route_id", sa.String(), primary_key=True),
        sa.Column("agency_id", sa.String(), nullable=True, index=True),
        sa.Column("short_name", sa.String(), nullable=True),
        sa.Column("long_name", sa.String(), nullable=True),
        sa.Column("route_type", sa.String(), nullable=True),
        sa.Column("source_provider", sa.String(), nullable=False),
        sa.Column("source_family", sa.String(), nullable=False),
        sa.Column("source_status", sa.String(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_url", sa.String(), nullable=True),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column("validation_note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "transit_stops",
        sa.Column("stop_id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("lat", sa.Float(), nullable=True),
        sa.Column("lon", sa.Float(), nullable=True),
        sa.Column("source_provider", sa.String(), nullable=False),
        sa.Column("source_family", sa.String(), nullable=False),
        sa.Column("source_status", sa.String(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_url", sa.String(), nullable=True),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column("validation_note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "transit_route_stops",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("route_id", sa.String(), sa.ForeignKey("transit_routes.route_id"), nullable=False, index=True),
        sa.Column("stop_id", sa.String(), sa.ForeignKey("transit_stops.stop_id"), nullable=False, index=True),
        sa.Column("stop_sequence", sa.Integer(), nullable=False),
        sa.Column("direction_id", sa.String(), nullable=True),
        sa.Column("variant_id", sa.String(), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("idx_transit_route_stops_route_seq", "transit_route_stops", ["route_id", "stop_sequence"])

    op.create_table(
        "transit_route_shapes",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("route_id", sa.String(), sa.ForeignKey("transit_routes.route_id"), nullable=False, index=True),
        sa.Column("variant_id", sa.String(), nullable=True, index=True),
        sa.Column("geom_geojson", postgresql.JSONB(), nullable=True),
        sa.Column("source_provider", sa.String(), nullable=False),
        sa.Column("source_family", sa.String(), nullable=False),
        sa.Column("source_status", sa.String(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "official_alerts",
        sa.Column("alert_id", sa.String(), primary_key=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("affected_mode", sa.String(), nullable=True),
        sa.Column("affected_route_id", sa.String(), nullable=True),
        sa.Column("affected_station_id", sa.String(), nullable=True),
        sa.Column("alert_category", sa.String(), nullable=True),
        sa.Column("severity", sa.String(), nullable=True),
        sa.Column("effective_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("effective_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_url", sa.String(), nullable=True),
        sa.Column("source_provider", sa.String(), nullable=False),
        sa.Column("source_family", sa.String(), nullable=False),
        sa.Column("source_status", sa.String(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column("validation_note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("idx_official_alerts_provider_time", "official_alerts", ["provider", "published_at"])

    op.create_table(
        "public_web_observations",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("provider_id", sa.String(), nullable=False, index=True),
        sa.Column("observation_type", sa.String(), nullable=False, index=True),
        sa.Column("subject_id", sa.String(), nullable=True, index=True),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("source_url", sa.String(), nullable=True),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column("validation_note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index(
        "idx_public_web_observations_provider_time",
        "public_web_observations",
        ["provider_id", "observed_at"],
    )

    op.create_table(
        "weather_observations",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("region_id", sa.String(), nullable=False, index=True),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("source_provider", sa.String(), nullable=False),
        sa.Column("source_family", sa.String(), nullable=False),
        sa.Column("source_status", sa.String(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_url", sa.String(), nullable=True),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column("validation_note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("idx_weather_observations_region_time", "weather_observations", ["region_id", "observed_at"])

    op.create_table(
        "digital_twin_snapshots",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("snapshot_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("data_status", sa.String(), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("provenance", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "anomaly_records",
        sa.Column("anomaly_id", sa.String(), primary_key=True),
        sa.Column("type", sa.String(), nullable=False, index=True),
        sa.Column("severity", sa.String(), nullable=False, index=True),
        sa.Column("segment_ids", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("zone_id", sa.String(), nullable=True, index=True),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("valid_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("recommended_response", sa.Text(), nullable=True),
        sa.Column("source_provider", sa.String(), nullable=False),
        sa.Column("source_family", sa.String(), nullable=False),
        sa.Column("source_status", sa.String(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_url", sa.String(), nullable=True),
        sa.Column("confidence", sa.String(), nullable=True),
        sa.Column("validation_note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "forecast_snapshots",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("horizon_minutes", sa.Integer(), nullable=False, index=True),
        sa.Column("segment_id", sa.String(), nullable=True, index=True),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("model_version", sa.String(), nullable=True),
        sa.Column("source_provider", sa.String(), nullable=False),
        sa.Column("source_family", sa.String(), nullable=False),
        sa.Column("source_status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("idx_forecast_snapshots_segment_time", "forecast_snapshots", ["segment_id", "generated_at"])


def downgrade() -> None:
    op.drop_index("idx_forecast_snapshots_segment_time", table_name="forecast_snapshots")
    op.drop_table("forecast_snapshots")
    op.drop_table("anomaly_records")
    op.drop_table("digital_twin_snapshots")
    op.drop_index("idx_weather_observations_region_time", table_name="weather_observations")
    op.drop_table("weather_observations")
    op.drop_index("idx_public_web_observations_provider_time", table_name="public_web_observations")
    op.drop_table("public_web_observations")
    op.drop_index("idx_official_alerts_provider_time", table_name="official_alerts")
    op.drop_table("official_alerts")
    op.drop_table("transit_route_shapes")
    op.drop_index("idx_transit_route_stops_route_seq", table_name="transit_route_stops")
    op.drop_table("transit_route_stops")
    op.drop_table("transit_stops")
    op.drop_table("transit_routes")


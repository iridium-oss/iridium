-- IRIDIUM baseline schema. PostgreSQL. PostGIS can be added for spatial queries.
-- This file is for reference and future migrations; the current API uses in-memory state.

-- Network nodes (segments, junctions, stops)
CREATE TABLE IF NOT EXISTS network_nodes (
    node_id TEXT PRIMARY KEY,
    node_type TEXT NOT NULL,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    name TEXT,
    mode TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Network edges
CREATE TABLE IF NOT EXISTS network_edges (
    edge_id TEXT PRIMARY KEY,
    from_node TEXT NOT NULL REFERENCES network_nodes(node_id),
    to_node TEXT NOT NULL REFERENCES network_nodes(node_id),
    mode TEXT NOT NULL,
    length_km DOUBLE PRECISION,
    travel_time_min DOUBLE PRECISION,
    cost DOUBLE PRECISION,
    carbon_kg DOUBLE PRECISION,
    speed_kmh DOUBLE PRECISION,
    occupancy_pct DOUBLE PRECISION,
    incident BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Observations (sensor, weather, etc.) for time-series and twin updates
CREATE TABLE IF NOT EXISTS observations (
    id BIGSERIAL PRIMARY KEY,
    source_type TEXT NOT NULL,
    segment_id TEXT,
    payload JSONB NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_observations_segment_time ON observations(segment_id, observed_at);
CREATE INDEX IF NOT EXISTS idx_observations_source ON observations(source_type, observed_at);

-- Forecast snapshots (cached forecasts)
CREATE TABLE IF NOT EXISTS forecast_snapshots (
    id BIGSERIAL PRIMARY KEY,
    horizon_minutes INT NOT NULL,
    segment_id TEXT,
    payload JSONB NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL,
    model_version TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_forecast_segment_time ON forecast_snapshots(segment_id, generated_at);

-- Anomalies
CREATE TABLE IF NOT EXISTS anomalies (
    anomaly_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    severity TEXT NOT NULL,
    segment_ids TEXT[],
    zone_id TEXT,
    detected_at TIMESTAMPTZ NOT NULL,
    valid_from TIMESTAMPTZ,
    valid_to TIMESTAMPTZ,
    description TEXT,
    recommended_response TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_anomalies_detected ON anomalies(detected_at);
CREATE INDEX IF NOT EXISTS idx_anomalies_type ON anomalies(type);

-- District scores (equity)
CREATE TABLE IF NOT EXISTS district_scores (
    id BIGSERIAL PRIMARY KEY,
    district_id TEXT NOT NULL,
    district_name TEXT,
    avg_travel_time_to_services_min DOUBLE PRECISION,
    pt_accessibility_proxy DOUBLE PRECISION,
    modal_availability_proxy DOUBLE PRECISION,
    affordability_proxy DOUBLE PRECISION,
    composite_score DOUBLE PRECISION,
    period_start TIMESTAMPTZ,
    period_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(district_id, period_start)
);

CREATE INDEX IF NOT EXISTS idx_district_scores_district ON district_scores(district_id);

-- PostGIS extension (required for network-import and spatial queries)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Provenance for network import (source timestamp and checksum)
CREATE TABLE IF NOT EXISTS network_import_manifest (
    id SERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_url TEXT,
    file_path TEXT,
    file_checksum_sha256 TEXT,
    fetched_at TIMESTAMPTZ,
    imported_at TIMESTAMPTZ DEFAULT NOW(),
    node_count INT DEFAULT 0,
    edge_count INT DEFAULT 0
);

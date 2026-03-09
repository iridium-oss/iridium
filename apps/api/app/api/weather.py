"""
Weather API: current, history, status.

Open-Meteo is a public API and does not require credentials for basic use.
This module does not fabricate weather data. If the provider is unavailable, data_status is explicit.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from iridium_schemas.events import WeatherSnapshot
from iridium_schemas.provenance import (
    DATA_STATUS_LIVE,
    DATA_STATUS_UNAVAILABLE,
    SourceProvenance,
)

router = APIRouter()


class WeatherCurrentResponse(BaseModel):
    data_status: str = Field(..., description="live or unavailable")
    fetched_at: datetime
    snapshots: list[WeatherSnapshot] = Field(default_factory=list)
    source_provenance: SourceProvenance


class WeatherHistoryResponse(BaseModel):
    data_status: str
    note: Optional[str] = None
    region_id: Optional[str] = None
    start_utc: Optional[datetime] = None
    end_utc: Optional[datetime] = None
    observations: list[WeatherSnapshot] = Field(default_factory=list)
    source_provenance: SourceProvenance


class WeatherStatusResponse(BaseModel):
    provider_id: str
    source_status: str
    data_status: str
    note: Optional[str] = None
    checked_at: datetime


@router.get(
    "/weather/current",
    response_model=WeatherCurrentResponse,
    summary="Current weather snapshot",
    description="Current weather for configured cities (Baku and Quba by default). Real data only.",
)
def get_current_weather() -> WeatherCurrentResponse:
    from weather_ingestion.open_meteo import fetch_weather

    result = fetch_weather(timeout_seconds=10.0)
    prov = result.to_provenance()
    return WeatherCurrentResponse(
        data_status=result.status,
        fetched_at=result.fetched_at or datetime.now(timezone.utc),
        snapshots=result.snapshots,
        source_provenance=prov,
    )


@router.get(
    "/weather/history",
    response_model=WeatherHistoryResponse,
    summary="Recent weather history",
    description=(
        "Returns stored recent weather observations when persistence is enabled. "
        "If persistence is not configured, returns data_status unavailable."
    ),
)
def get_weather_history(
    region_id: Optional[str] = Query(None, description="City or region identifier (baku, quba)"),
    start_utc: Optional[datetime] = Query(None, description="Start timestamp (UTC)"),
    end_utc: Optional[datetime] = Query(None, description="End timestamp (UTC)"),
) -> WeatherHistoryResponse:
    now = datetime.now(timezone.utc)
    return WeatherHistoryResponse(
        data_status=DATA_STATUS_UNAVAILABLE,
        note="Weather history storage is not configured in this deployment",
        region_id=region_id,
        start_utc=start_utc,
        end_utc=end_utc,
        observations=[],
        source_provenance=SourceProvenance(
            source_name="open_meteo",
            status=DATA_STATUS_UNAVAILABLE,
            fetched_at=now,
            provider="Open-Meteo",
            note="No persisted weather history available",
        ),
    )


@router.get(
    "/weather/status",
    response_model=WeatherStatusResponse,
    summary="Weather provider status",
    description="Reports whether the weather provider can be reached. Does not fabricate data.",
)
def get_weather_status() -> WeatherStatusResponse:
    from weather_ingestion.open_meteo import fetch_weather

    now = datetime.now(timezone.utc)
    result = fetch_weather(timeout_seconds=6.0)
    return WeatherStatusResponse(
        provider_id="open_meteo",
        source_status="public_api",
        data_status=DATA_STATUS_LIVE if result.status == DATA_STATUS_LIVE else DATA_STATUS_UNAVAILABLE,
        note=result.note,
        checked_at=now,
    )


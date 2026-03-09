"""
System endpoints: status, data sources, and provenance.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter()


@router.get(
    "/system/status",
    summary="System status",
    description="High-level system status and enabled subsystems. Never implies data availability.",
)
def get_system_status() -> dict:
    settings = get_settings()
    now = datetime.now(timezone.utc).isoformat()
    return {
        "service": settings.core.app_name,
        "version": settings.core.app_version,
        "environment": settings.core.environment,
        "time_utc": now,
        "subsystems": {
            "database": {"enabled": settings.db.enabled},
            "cache": {"enabled": settings.cache.enabled},
            "providers": {
                "open_meteo": {"enabled": settings.providers.open_meteo_enabled},
                "yandex_observed": {"enabled": settings.providers.yandex_observed_enabled},
                "twogis": {"enabled": settings.providers.twogis_enabled},
                "moovit": {"enabled": settings.providers.moovit_enabled},
            },
        },
        "note": "Status reports configuration only. Data availability is exposed per endpoint via data_status and provenance.",
    }


@router.get(
    "/system/data-sources",
    summary="Configured data sources",
    description="Declared data sources and their intended source_status semantics. Does not claim availability.",
)
def get_data_sources() -> dict:
    return {
        "sources": [
            {
                "provider_id": "open_meteo",
                "source_family": "public_api",
                "source_status": "public_api",
                "note": "Public weather API. Subject to rate limits and availability.",
            },
            {
                "provider_id": "bakubus_official_alerts",
                "source_family": "official_website",
                "source_status": "official_alerts_only",
                "note": "Official website alerts. Not GTFS Realtime.",
            },
            {
                "provider_id": "bakumetro_official_alerts",
                "source_family": "official_website",
                "source_status": "official_alerts_only",
                "note": "Official website alerts. Not GTFS Realtime.",
            },
            {
                "provider_id": "bakubus_ayna",
                "source_family": "public_undocumented",
                "source_status": "public_undocumented",
                "note": "Public undocumented endpoint. Semantics may change without notice.",
            },
            {
                "provider_id": "yandex_transport_observed",
                "source_family": "public_web_observed",
                "source_status": "public_web_observed",
                "note": "Public web observed pages. Not an operator feed.",
            },
            {
                "provider_id": "yandex_metro_operational",
                "source_family": "public_web_operational_context",
                "source_status": "public_web_operational_context",
                "note": "Public web operational context. Not an operator feed.",
            },
            {
                "provider_id": "twogis_public_transport",
                "source_family": "licensed_partner",
                "source_status": "licensed_partner",
                "note": "Licensed partner integration. Requires credentials.",
            },
            {
                "provider_id": "moovit_partner",
                "source_family": "licensed_partner",
                "source_status": "permission_required",
                "note": "Partner integration requires permissions and credentials.",
            },
        ]
    }


@router.get(
    "/system/data-provenance",
    summary="Data provenance policy",
    description="Explains provenance fields present in API responses and how missing data is represented.",
)
def get_data_provenance() -> dict:
    return {
        "policy": {
            "real_source_only": True,
            "no_fabrication": True,
            "missing_data_is_explicit": True,
        },
        "fields": [
            "source_provider",
            "source_family",
            "source_status",
            "fetched_at_or_observed_at",
            "source_url",
            "confidence",
            "validation_note",
        ],
        "notes": [
            "Endpoints must expose data_status fields when required inputs are missing.",
            "Public web observed outputs are not equivalent to operator realtime feeds.",
        ],
    }


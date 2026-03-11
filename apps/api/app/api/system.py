"""
System endpoints: status, data sources, provenance, and unified provider registry.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.providers.registry import (
    get_all_providers,
    get_provider,
    check_provider_health,
    verify_provider,
    get_integrations_status,
    get_integrations_report,
)

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


@router.get(
    "/system/providers",
    summary="Unified provider registry",
    description="All external APIs and data sources with source_family, capabilities, and validation status.",
)
def list_providers() -> dict:
    providers = get_all_providers()
    return {
        "providers": [
            {
                "id": p.id,
                "display_name": p.display_name,
                "source_family": p.source_family,
                "source_status": p.source_status,
                "domain": p.domain,
                "required_env_vars": p.required_env_vars,
                "healthcheck_mode": p.healthcheck_mode,
                "backend_adapter_module": p.backend_adapter_module,
                "frontend_consumer_surfaces": p.frontend_consumer_surfaces,
                "capabilities": p.capabilities.to_dict(),
                "last_checked_at": p.last_checked_at.isoformat() if p.last_checked_at else None,
                "validation_status": p.validation_status,
                "note": p.note,
            }
            for p in providers
        ],
        "total": len(providers),
    }


@router.get(
    "/system/providers/{provider_id}",
    summary="Provider by id",
    description="Single provider entry from registry. 404 if unknown.",
)
def get_provider_by_id(provider_id: str) -> dict:
    p = get_provider(provider_id)
    if not p:
        raise HTTPException(status_code=404, detail={"error": "not_found", "message": "Unknown provider id"})
    return {
        "id": p.id,
        "display_name": p.display_name,
        "source_family": p.source_family,
        "source_status": p.source_status,
        "domain": p.domain,
        "required_env_vars": p.required_env_vars,
        "healthcheck_mode": p.healthcheck_mode,
        "backend_adapter_module": p.backend_adapter_module,
        "frontend_consumer_surfaces": p.frontend_consumer_surfaces,
        "capabilities": p.capabilities.to_dict(),
        "last_checked_at": p.last_checked_at.isoformat() if p.last_checked_at else None,
        "validation_status": p.validation_status,
        "note": p.note,
    }


@router.get(
    "/system/providers/{provider_id}/health",
    summary="Provider health",
    description="Current health/validation status for the provider. Runs verification.",
)
def provider_health(provider_id: str) -> dict:
    return check_provider_health(provider_id)


@router.post(
    "/system/providers/{provider_id}/verify",
    summary="Verify provider",
    description="Run verification (e.g. sample request) for the provider. Returns validation_status.",
)
def provider_verify(provider_id: str) -> dict:
    if not get_provider(provider_id):
        raise HTTPException(status_code=404, detail={"error": "not_found", "message": "Unknown provider id"})
    validation_status, last_checked_at, message = verify_provider(provider_id)
    return {
        "provider_id": provider_id,
        "validation_status": validation_status,
        "last_checked_at": last_checked_at.isoformat() if last_checked_at else None,
        "message": message,
    }


@router.get(
    "/system/integrations/status",
    summary="Integrations status",
    description="Aggregate status of all providers by domain. No live checks.",
)
def integrations_status() -> dict:
    return get_integrations_status()


@router.get(
    "/system/integrations/report",
    summary="Integrations report",
    description="Full report with verification result per provider. Runs live checks; may be slow.",
)
def integrations_report() -> dict:
    return get_integrations_report()


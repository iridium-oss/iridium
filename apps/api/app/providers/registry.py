"""
Unified provider registry for all external APIs and data sources.

Each provider has: id, display_name, source_family, source_status, required_env_vars,
healthcheck_mode, capabilities, and verification logic. No fabricated status.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

VALIDATION_WORKING = "working"
VALIDATION_PARTIALLY_WORKING = "partially_working"
VALIDATION_CONFIGURATION_REQUIRED = "configuration_required"
VALIDATION_PERMISSION_REQUIRED = "permission_required"
VALIDATION_UNAVAILABLE = "unavailable"
VALIDATION_DEPRECATED = "deprecated"
VALIDATION_STALE_CONFIGURATION = "stale_configuration"
VALIDATION_ENDPOINT_CHANGED = "endpoint_changed"
VALIDATION_NOT_CHECKED = "not_checked"


@dataclass
class ProviderCapabilities:
    supports_search: bool = False
    supports_metadata: bool = False
    supports_tiles: bool = False
    supports_routing: bool = False
    supports_alerts: bool = False
    supports_realtime: bool = False
    supports_historical: bool = False
    supports_analytics: bool = False
    supports_auth: bool = False
    supports_web_observation: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "supports_search": self.supports_search,
            "supports_metadata": self.supports_metadata,
            "supports_tiles": self.supports_tiles,
            "supports_routing": self.supports_routing,
            "supports_alerts": self.supports_alerts,
            "supports_realtime": self.supports_realtime,
            "supports_historical": self.supports_historical,
            "supports_analytics": self.supports_analytics,
            "supports_auth": self.supports_auth,
            "supports_web_observation": self.supports_web_observation,
        }


@dataclass
class ProviderEntry:
    id: str
    display_name: str
    source_family: str
    source_status: str
    required_env_vars: list[str] = field(default_factory=list)
    healthcheck_mode: str = "on_demand"
    backend_adapter_module: str = ""
    frontend_consumer_surfaces: list[str] = field(default_factory=list)
    capabilities: ProviderCapabilities = field(default_factory=ProviderCapabilities)
    last_checked_at: datetime | None = None
    validation_status: str = VALIDATION_NOT_CHECKED
    note: str = ""
    domain: str = ""


def _build_registry() -> list[ProviderEntry]:
    return [
        ProviderEntry(
            id="open_meteo",
            display_name="Open-Meteo",
            source_family="public_api",
            source_status="public_api",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="weather_ingestion.open_meteo",
            frontend_consumer_surfaces=["dashboard", "weather", "digital_twin_context"],
            capabilities=ProviderCapabilities(supports_metadata=True, supports_historical=True),
            note="Public weather API. No key required. Subject to rate limits.",
            domain="weather",
        ),
        ProviderEntry(
            id="copernicus_stac",
            display_name="Copernicus Data Space STAC",
            source_family="stac_catalog",
            source_status="public_api",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="earth_observation.sentinel2.providers.copernicus_stac",
            frontend_consumer_surfaces=["dashboard/satellite", "eo_overlays"],
            capabilities=ProviderCapabilities(supports_search=True, supports_metadata=True),
            note="Primary Sentinel-2 catalog. STAC only; OpenSearch deprecated after 2 March 2026.",
            domain="earth_observation",
        ),
        ProviderEntry(
            id="earth_search_stac",
            display_name="Earth Search STAC",
            source_family="stac_catalog",
            source_status="public_api",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="earth_observation.sentinel2.providers.earth_search_stac",
            frontend_consumer_surfaces=["dashboard/satellite", "eo_overlays"],
            capabilities=ProviderCapabilities(supports_search=True, supports_metadata=True),
            note="Fallback Sentinel-2 L2A catalog. No auth.",
            domain="earth_observation",
        ),
        ProviderEntry(
            id="sentinel_hub",
            display_name="Sentinel Hub Process API",
            source_family="licensed_partner",
            source_status="configuration_required",
            required_env_vars=["IRIDIUM_EO__SENTINEL_HUB_INSTANCE_ID"],
            healthcheck_mode="on_demand",
            backend_adapter_module="",
            frontend_consumer_surfaces=["dashboard/satellite"],
            capabilities=ProviderCapabilities(
                supports_tiles=True, supports_analytics=True, supports_auth=True
            ),
            note="Optional. For tile rendering and statistics when configured.",
            domain="earth_observation",
        ),
        ProviderEntry(
            id="bakubus_ayna",
            display_name="BakuBus (AYNA API)",
            source_family="public_undocumented",
            source_status="public_undocumented",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.bakubus_ayna",
            frontend_consumer_surfaces=["dashboard/transit", "transit_routes", "provider_status"],
            capabilities=ProviderCapabilities(supports_metadata=True, supports_realtime=True),
            note="Public AYNA getBusList; getBusById public undocumented.",
            domain="transit",
        ),
        ProviderEntry(
            id="bakumetro_official",
            display_name="Baku Metro (official website)",
            source_family="official_website",
            source_status="static_schedule_only",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.bakumetro_official",
            frontend_consumer_surfaces=["dashboard/transit", "transit_routes", "provider_status"],
            capabilities=ProviderCapabilities(supports_metadata=True),
            note="Static network from official site. No machine-readable GTFS from operator.",
            domain="transit",
        ),
        ProviderEntry(
            id="bakubus_official_alerts",
            display_name="BakuBus official alerts",
            source_family="official_website",
            source_status="official_alerts_only",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.bakubus_official_alerts",
            frontend_consumer_surfaces=["alerts", "dashboard/transit", "provider_status"],
            capabilities=ProviderCapabilities(supports_alerts=True),
            note="Official website news/notifications. Not GTFS Realtime.",
            domain="transit",
        ),
        ProviderEntry(
            id="bakumetro_official_alerts",
            display_name="Baku Metro official alerts",
            source_family="official_website",
            source_status="official_alerts_only",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.bakumetro_official_alerts",
            frontend_consumer_surfaces=["alerts", "dashboard/transit", "provider_status"],
            capabilities=ProviderCapabilities(supports_alerts=True),
            note="Official website service updates. Not GTFS Realtime.",
            domain="transit",
        ),
        ProviderEntry(
            id="yandex_transport_observed",
            display_name="Yandex transport (public web observed)",
            source_family="public_web_observed",
            source_status="public_web_observed",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.yandex_transport_observed",
            frontend_consumer_surfaces=["dashboard/transit", "live_arrivals", "provider_status"],
            capabilities=ProviderCapabilities(
                supports_metadata=True, supports_realtime=True, supports_web_observation=True
            ),
            note="Stop-level predictions from Yandex Baku pages. Not operator feed.",
            domain="transit",
        ),
        ProviderEntry(
            id="yandex_metro_operational",
            display_name="Yandex Metro operational context",
            source_family="public_web_operational_context",
            source_status="public_web_operational_context",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.yandex_metro_operational",
            frontend_consumer_surfaces=["dashboard/transit", "provider_status"],
            capabilities=ProviderCapabilities(
                supports_metadata=True, supports_web_observation=True
            ),
            note="Closed stations etc. from Yandex Metro Baku. Not operator feed.",
            domain="transit",
        ),
        ProviderEntry(
            id="yandex_traffic_context",
            display_name="Yandex traffic context",
            source_family="public_web_observed",
            source_status="configuration_required",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.yandex_traffic_context",
            frontend_consumer_surfaces=[],
            capabilities=ProviderCapabilities(supports_web_observation=True),
            note="Traffic context adapter. Status from get_traffic_context_status.",
            domain="transit",
        ),
        ProviderEntry(
            id="twogis_public_transport",
            display_name="2GIS Public Transport API",
            source_family="licensed_partner",
            source_status="configuration_required",
            required_env_vars=["IRIDIUM_TWOGIS__API_KEY"],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.twogis_public_transport",
            frontend_consumer_surfaces=["dashboard/transit", "routing", "provider_status"],
            capabilities=ProviderCapabilities(
                supports_routing=True, supports_metadata=True, supports_auth=True
            ),
            note="Licensed partner. Requires API key when enabled.",
            domain="transit",
        ),
        ProviderEntry(
            id="moovit_partner",
            display_name="Moovit partner",
            source_family="licensed_partner",
            source_status="permission_required",
            required_env_vars=["IRIDIUM_MOOVIT__API_KEY"],
            healthcheck_mode="on_demand",
            backend_adapter_module="transit_ingestion.providers.moovit_partner",
            frontend_consumer_surfaces=["dashboard/transit", "provider_status"],
            capabilities=ProviderCapabilities(supports_metadata=True, supports_auth=True),
            note="Partner integration. Interface only until credentials configured.",
            domain="transit",
        ),
        ProviderEntry(
            id="traffic_provider",
            display_name="Traffic provider (e.g. TomTom)",
            source_family="licensed_partner",
            source_status="configuration_required",
            required_env_vars=["TRAFFIC_API_KEY", "TOMTOM_API_KEY"],
            healthcheck_mode="on_demand",
            backend_adapter_module="traffic_provider",
            frontend_consumer_surfaces=[],
            capabilities=ProviderCapabilities(supports_metadata=True, supports_auth=True),
            note="Not wired to API. Adapter exists in services/traffic-provider.",
            domain="traffic",
        ),
        ProviderEntry(
            id="traccar",
            display_name="Traccar telemetry",
            source_family="permission_required",
            source_status="configuration_required",
            required_env_vars=[
                "IRIDIUM_TELEMETRY__TRACCAR_HOST",
                "IRIDIUM_TELEMETRY__TRACCAR_USER",
                "IRIDIUM_TELEMETRY__TRACCAR_PASSWORD",
            ],
            healthcheck_mode="on_demand",
            backend_adapter_module="",
            frontend_consumer_surfaces=[],
            capabilities=ProviderCapabilities(supports_realtime=True, supports_auth=True),
            note="Consent-based device ingestion. Unavailable until configured.",
            domain="telemetry",
        ),
        ProviderEntry(
            id="network_import",
            display_name="Network import (PostGIS/OSM)",
            source_family="public_api",
            source_status="configuration_required",
            required_env_vars=["IRIDIUM_DB__DSN"],
            healthcheck_mode="on_demand",
            backend_adapter_module="network_import.db_loader",
            frontend_consumer_surfaces=["dashboard/network", "digital_twin", "routing"],
            capabilities=ProviderCapabilities(supports_metadata=True),
            note="OSM PBF loaded into PostGIS. Graph empty until import run and DB enabled.",
            domain="network",
        ),
        ProviderEntry(
            id="bakikart",
            display_name="BakıKart",
            source_family="permission_required",
            source_status="permission_required",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="",
            frontend_consumer_surfaces=[],
            capabilities=ProviderCapabilities(supports_metadata=True, supports_auth=True),
            note="Payment context, QR, validator, portal model. Not implemented; permission or partner required.",
            domain="transit",
        ),
        ProviderEntry(
            id="iticket",
            display_name="iTicket",
            source_family="permission_required",
            source_status="permission_required",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="",
            frontend_consumer_surfaces=[],
            capabilities=ProviderCapabilities(supports_metadata=True),
            note="Events, venues, event dates, category, venue address, QR/e-ticket. See docs/event-sources.md. Not implemented.",
            domain="events",
        ),
        ProviderEntry(
            id="gomap_api",
            display_name="GoMap API",
            source_family="configuration_required",
            source_status="configuration_required",
            required_env_vars=[],
            healthcheck_mode="on_demand",
            backend_adapter_module="",
            frontend_consumer_surfaces=[],
            capabilities=ProviderCapabilities(
                supports_search=True, supports_routing=True, supports_metadata=True
            ),
            note="Search, region lookup, route XML. Not implemented; add when API or partnership available.",
            domain="map_routing",
        ),
    ]


_PROVIDERS: list[ProviderEntry] | None = None


def get_all_providers() -> list[ProviderEntry]:
    global _PROVIDERS
    if _PROVIDERS is None:
        _PROVIDERS = _build_registry()
    return list(_PROVIDERS)


def get_provider(provider_id: str) -> ProviderEntry | None:
    for p in get_all_providers():
        if p.id == provider_id:
            return p
    return None


def _verify_open_meteo() -> tuple[str, datetime | None]:
    try:
        from weather_ingestion.open_meteo import fetch_weather

        r = fetch_weather(timeout_seconds=5.0)
        if r.status == "live" and r.snapshots:
            return VALIDATION_WORKING, datetime.now(UTC)
        if r.status == "unavailable":
            return VALIDATION_UNAVAILABLE, datetime.now(UTC)
        return VALIDATION_PARTIALLY_WORKING, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _verify_copernicus_stac() -> tuple[str, datetime | None]:
    try:
        from earth_observation.sentinel2.providers.copernicus_stac import CopernicusStacProvider
        from iridium_schemas.earth_observation import EOSourceStatus

        p = CopernicusStacProvider()
        s = p.status()
        if s == EOSourceStatus.live:
            return VALIDATION_WORKING, datetime.now(UTC)
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _verify_earth_search_stac() -> tuple[str, datetime | None]:
    try:
        from earth_observation.sentinel2.providers.earth_search_stac import EarthSearchStacProvider
        from iridium_schemas.earth_observation import EOSourceStatus

        p = EarthSearchStacProvider()
        s = p.status()
        if s == EOSourceStatus.live:
            return VALIDATION_WORKING, datetime.now(UTC)
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _verify_bakubus_ayna() -> tuple[str, datetime | None]:
    try:
        from transit_ingestion.providers.bakubus_ayna import fetch_bus_list

        result = fetch_bus_list(timeout=8.0)
        if result is not None and getattr(result, "error", None) is None:
            return VALIDATION_WORKING, datetime.now(UTC)
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _verify_bakumetro_official() -> tuple[str, datetime | None]:
    try:
        from transit_ingestion.providers.bakumetro_official import (
            get_metro_lines,
            get_metro_stations,
        )

        lines = get_metro_lines()
        stations = get_metro_stations()
        if (lines and len(lines) > 0) or (stations and len(stations) > 0):
            return VALIDATION_WORKING, datetime.now(UTC)
        return VALIDATION_PARTIALLY_WORKING, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _verify_alerts(module_name: str) -> tuple[str, datetime | None]:
    try:
        if "bakubus" in module_name:
            from transit_ingestion.providers.bakubus_official_alerts import fetch_bakubus_alerts

            alerts = fetch_bakubus_alerts(timeout=10.0)
        else:
            from transit_ingestion.providers.bakumetro_official_alerts import fetch_metro_alerts

            alerts = fetch_metro_alerts(timeout=10.0)
        return VALIDATION_WORKING, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _verify_twogis() -> tuple[str, datetime | None]:
    try:
        from transit_ingestion.providers.twogis_public_transport import (
            fetch_route_alternatives,
            get_twogis_status,
        )

        if get_twogis_status() != "configured":
            return VALIDATION_CONFIGURATION_REQUIRED, datetime.now(UTC)
        # Minimal verification: Baku area short route request
        results = fetch_route_alternatives(40.4093, 49.8671, 40.3764, 49.8530, timeout=10.0)
        if results is not None:
            return VALIDATION_WORKING, datetime.now(UTC)
        return VALIDATION_PARTIALLY_WORKING, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _verify_moovit() -> tuple[str, datetime | None]:
    try:
        from transit_ingestion.providers.moovit_partner import get_moovit_config

        cfg = get_moovit_config()
        if not cfg.enabled:
            return VALIDATION_CONFIGURATION_REQUIRED, datetime.now(UTC)
        # Adapter is interface-only; no real API call yet
        return VALIDATION_PARTIALLY_WORKING, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _verify_sentinel_hub() -> tuple[str, datetime | None]:
    """Check Sentinel Hub: instance_id + client credentials; try OAuth2 token."""
    try:
        from app.config import get_settings

        settings = get_settings()
        instance_id = settings.eo.sentinel_hub_instance_id
        cid = settings.eo.sentinel_hub_client_id
        csec = settings.eo.sentinel_hub_client_secret
        client_id = cid.get_secret_value() if cid else None
        client_secret = csec.get_secret_value() if csec else None
        if not instance_id:
            return VALIDATION_CONFIGURATION_REQUIRED, datetime.now(UTC)
        if not client_id or not client_secret:
            return VALIDATION_CONFIGURATION_REQUIRED, datetime.now(UTC)
        import httpx

        r = httpx.post(
            "https://auth.sentinel-hub.com/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10.0,
        )
        if r.status_code == 200 and r.json().get("access_token"):
            return VALIDATION_WORKING, datetime.now(UTC)
        return VALIDATION_PARTIALLY_WORKING, datetime.now(UTC)
    except Exception:
        return VALIDATION_UNAVAILABLE, datetime.now(UTC)


def _credential_satisfied(provider_id: str, required: list[str]) -> bool:
    """Return True if any of the required or legacy env vars for this provider are set."""
    import os

    legacy_map = {
        "twogis_public_transport": ["IRIDIUM_TWOGIS__API_KEY", "TWOGIS_API_KEY"],
        "moovit_partner": ["IRIDIUM_MOOVIT__API_KEY", "MOOVIT_API_KEY", "MOOVIT_PARTNER_API_KEY"],
    }
    keys_to_check = list(required) if required else []
    keys_to_check.extend(legacy_map.get(provider_id, []))
    return any(os.environ.get(k) for k in keys_to_check)


def verify_provider(provider_id: str) -> tuple[str, datetime | None, str]:
    """
    Run verification for a provider. Returns (validation_status, last_checked_at, message).
    Does not mutate global state; caller can store last_checked_at.
    """

    entry = get_provider(provider_id)
    if not entry:
        return VALIDATION_UNAVAILABLE, None, "Unknown provider id"
    if entry.required_env_vars and not _credential_satisfied(provider_id, entry.required_env_vars):
        return (
            VALIDATION_CONFIGURATION_REQUIRED,
            datetime.now(UTC),
            "Missing credentials (set API key or partner env)",
        )
    handlers = {
        "open_meteo": _verify_open_meteo,
        "copernicus_stac": _verify_copernicus_stac,
        "earth_search_stac": _verify_earth_search_stac,
        "bakubus_ayna": _verify_bakubus_ayna,
        "bakumetro_official": _verify_bakumetro_official,
        "bakubus_official_alerts": lambda: _verify_alerts("bakubus"),
        "bakumetro_official_alerts": lambda: _verify_alerts("bakumetro"),
        "twogis_public_transport": _verify_twogis,
        "moovit_partner": _verify_moovit,
        "sentinel_hub": _verify_sentinel_hub,
    }
    handler = handlers.get(provider_id)
    if not handler:
        return VALIDATION_NOT_CHECKED, datetime.now(UTC), "No verification implemented"
    status, checked = handler()
    return status, checked, status


def check_provider_health(provider_id: str) -> dict[str, Any]:
    """Return health dict for provider: status, last_checked_at, message, validation_status."""
    entry = get_provider(provider_id)
    if not entry:
        return {
            "provider_id": provider_id,
            "validation_status": VALIDATION_UNAVAILABLE,
            "message": "Unknown provider",
        }
    validation_status, last_checked_at, message = verify_provider(provider_id)
    return {
        "provider_id": provider_id,
        "display_name": entry.display_name,
        "validation_status": validation_status,
        "last_checked_at": last_checked_at.isoformat() if last_checked_at else None,
        "message": message,
        "source_family": entry.source_family,
        "source_status": entry.source_status,
    }


def get_integrations_status() -> dict[str, Any]:
    """Aggregate status of all providers by domain. No fabricated counts."""
    providers = get_all_providers()
    by_domain: dict[str, list[dict[str, Any]]] = {}
    for p in providers:
        domain = p.domain or "other"
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(
            {
                "id": p.id,
                "display_name": p.display_name,
                "source_family": p.source_family,
                "source_status": p.source_status,
                "validation_status": p.validation_status,
                "required_env_vars": p.required_env_vars,
            }
        )
    return {
        "domains": by_domain,
        "total_providers": len(providers),
        "note": "Validation status may be not_checked until verify is called per provider.",
    }


def get_integrations_report() -> dict[str, Any]:
    """Full report: each provider with health result. Runs verification for all that support it."""
    providers = get_all_providers()
    results = []
    for p in providers:
        status, checked, msg = verify_provider(p.id)
        results.append(
            {
                "provider_id": p.id,
                "display_name": p.display_name,
                "domain": p.domain,
                "source_family": p.source_family,
                "source_status": p.source_status,
                "validation_status": status,
                "last_checked_at": checked.isoformat() if checked else None,
                "message": msg,
                "required_env_vars": p.required_env_vars,
                "capabilities": p.capabilities.to_dict(),
            }
        )
    return {
        "report_generated_at": datetime.now(UTC).isoformat(),
        "providers": results,
        "note": "Verification runs live checks. Failures indicate provider unreachable or misconfigured.",
    }

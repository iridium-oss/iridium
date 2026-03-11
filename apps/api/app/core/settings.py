"""
Typed application settings.

Settings are grouped by subsystem and loaded from environment variables.
Nested settings use env_nested_delimiter="__".
Example: IRIDIUM_DB__DSN, IRIDIUM_CACHE__REDIS_URL.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, SecretStr
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CoreAppSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    environment: str = Field("development", description="Runtime environment name")
    app_name: str = Field("iridium-api", description="Service identifier")
    app_version: str = Field("0.1.0-dev", description="Service version string")

    api_host: str = Field("0.0.0.0", description="Bind host")
    api_port: int = Field(8000, description="Bind port")
    api_base_url: str = Field("http://localhost:8000", description="External base URL")

    cors_origins: str = Field(
        "http://localhost:3000,http://127.0.0.1:3000",
        description="Comma-separated list of allowed CORS origins",
    )
    cors_allow_credentials: bool = Field(
        False,
        description="Whether CORS responses allow credentials. Prefer false unless required.",
    )
    cors_allow_methods: str = Field(
        "GET,POST,OPTIONS",
        description="Comma-separated list of allowed CORS methods",
    )
    cors_allow_headers: str = Field(
        "Authorization,Content-Type,X-Request-ID",
        description="Comma-separated list of allowed CORS request headers",
    )

    max_request_body_bytes: int = Field(
        1024 * 1024,
        description="Maximum request body size in bytes. Enforced using Content-Length when present.",
    )

    hsts_enabled: bool = Field(
        False,
        description="Enable Strict-Transport-Security header. Only enable behind TLS.",
    )
    hsts_max_age_seconds: int = Field(
        31536000,
        description="HSTS max-age in seconds when enabled",
    )
    log_level: str = Field("INFO", description="Log level")

    data_samples_dir: str = Field("data/samples", description="Recorded or sample data directory")
    data_synthetic_dir: str = Field("data/synthetic", description="Synthetic data directory for tests")
    equity_data_path: str = Field("", description="Path to recorded equity data directory")

    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def cors_allow_methods_list(self) -> list[str]:
        return [m.strip().upper() for m in self.cors_allow_methods.split(",") if m.strip()]

    def cors_allow_headers_list(self) -> list[str]:
        return [h.strip() for h in self.cors_allow_headers.split(",") if h.strip()]

    def data_samples_path(self) -> Path:
        return Path(self.data_samples_dir)

    def data_synthetic_path(self) -> Path:
        return Path(self.data_synthetic_dir)

    def equity_path(self) -> Optional[Path]:
        p = Path(self.equity_data_path).resolve() if self.equity_data_path else None
        return p if p and p.exists() else None


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(False, description="Enable database integration")
    dsn: Optional[SecretStr] = Field(
        default=None,
        description="PostgreSQL DSN, for example postgresql+psycopg://user:pass@host:5432/db",
    )


class CacheSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(False, description="Enable Redis caching")
    redis_url: Optional[SecretStr] = Field(default=None, description="Redis URL")


class ProviderSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    open_meteo_enabled: bool = Field(True, description="Enable Open-Meteo integration")
    yandex_observed_enabled: bool = Field(True, description="Enable public-web observed sources")
    twogis_enabled: bool = Field(False, description="Enable 2GIS integration when configured")
    moovit_enabled: bool = Field(False, description="Enable Moovit integration when configured")


class NetworkImportSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(False, description="Enable network import and DB-backed network graph")
    osm_data_dir: str = Field(
        "data/manifests/osm",
        description="Directory for OSM raw sources and manifest",
    )


class WeatherSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(True, description="Enable weather provider integration")
    provider_id: str = Field("open_meteo", description="Weather provider identifier")
    timeout_seconds: float = Field(10.0, ge=1.0, le=60.0, description="Weather provider timeout")
    cache_ttl_seconds: int = Field(300, ge=0, le=86400, description="Cache TTL for weather responses")


class TransitSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(True, description="Enable transit aggregation endpoints")
    bakubus_ayna_enabled: bool = Field(True, description="Enable AYNA public-undocumented connector")
    yandex_observed_enabled: bool = Field(True, description="Enable Yandex public-web observed connector")
    cache_ttl_seconds: int = Field(120, ge=0, le=86400, description="Cache TTL for web observed sources")


class YandexObservedSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(True, description="Enable Yandex public-web observed sources")
    default_stop_url: str = Field(
        "",
        description="Optional default stop URL for observed arrivals. Leave empty to require explicit URL.",
    )
    timeout_seconds: float = Field(8.0, ge=1.0, le=60.0)


class TwoGisSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(False, description="Enable 2GIS partner integration")
    api_key: Optional[SecretStr] = Field(default=None, description="2GIS API key (partner)")
    base_url: str = Field("", description="2GIS API base URL when applicable")


class MoovitSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(False, description="Enable Moovit partner integration")
    api_key: Optional[SecretStr] = Field(default=None, description="Moovit API key (partner)")
    base_url: str = Field("", description="Moovit API base URL when applicable")


class TelemetrySettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(False, description="Enable telemetry ingestion from a consent-based system")
    traccar_host: str = Field("", description="Traccar base URL")
    traccar_user: Optional[SecretStr] = Field(default=None, description="Traccar username")
    traccar_password: Optional[SecretStr] = Field(default=None, description="Traccar password")


class ObservabilitySettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    metrics_enabled: bool = Field(False, description="Enable Prometheus-style metrics endpoint")
    log_http_timing: bool = Field(True, description="Log request timing data")


class EarthObservationSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    enabled: bool = Field(True, description="Enable earth observation (Sentinel-2) endpoints")
    prefer_copernicus: bool = Field(True, description="Use Copernicus STAC first, then Earth Search")
    copernicus_stac_url: str = Field(
        "https://catalogue.dataspace.copernicus.eu/stac",
        description="Copernicus Data Space Ecosystem STAC base URL",
    )
    earth_search_stac_url: str = Field(
        "https://earth-search.aws.element84.com/v1",
        description="Earth Search STAC base URL (fallback)",
    )
    search_cache_ttl_seconds: int = Field(300, ge=0, le=86400, description="Scene search cache TTL")
    sentinel_hub_instance_id: Optional[str] = Field(None, description="Sentinel Hub instance ID for Process API when set")
    sentinel_hub_base_url: Optional[str] = Field(None, description="Sentinel Hub Process API base URL when set")
    sentinel_hub_client_id: Optional[SecretStr] = Field(None, description="Sentinel Hub OAuth2 client ID for token acquisition")
    sentinel_hub_client_secret: Optional[SecretStr] = Field(None, description="Sentinel Hub OAuth2 client secret")
    cdse_username: Optional[SecretStr] = Field(None, description="Copernicus Data Space username for authenticated STAC")
    cdse_password: Optional[SecretStr] = Field(None, description="Copernicus Data Space password")
    cdse_client_id: Optional[SecretStr] = Field(None, description="CDSE OAuth2 client ID (alternative to username/password)")
    cdse_client_secret: Optional[SecretStr] = Field(None, description="CDSE OAuth2 client secret")


class GoMapSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    api_key: Optional[SecretStr] = Field(None, description="GoMap API key when integration is enabled")
    base_url: str = Field("", description="GoMap API base URL when set")
    allowed_server_ip: Optional[str] = Field(None, description="Optional server IP allowlist for GoMap")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="IRIDIUM_",
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    core: CoreAppSettings = Field(default_factory=CoreAppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    providers: ProviderSettings = Field(default_factory=ProviderSettings)
    network: NetworkImportSettings = Field(default_factory=NetworkImportSettings)
    weather: WeatherSettings = Field(default_factory=WeatherSettings)
    transit: TransitSettings = Field(default_factory=TransitSettings)
    yandex: YandexObservedSettings = Field(default_factory=YandexObservedSettings)
    twogis: TwoGisSettings = Field(default_factory=TwoGisSettings)
    moovit: MoovitSettings = Field(default_factory=MoovitSettings)
    telemetry: TelemetrySettings = Field(default_factory=TelemetrySettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)
    eo: EarthObservationSettings = Field(default_factory=EarthObservationSettings)
    gomap: GoMapSettings = Field(default_factory=GoMapSettings)

    @model_validator(mode="before")
    @classmethod
    def _map_legacy_init_keys(cls, data):
        """
        Preserve compatibility for direct construction and older tests.

        This maps legacy top level keys (for example CORS_ORIGINS) into the nested Settings model.
        """
        if not isinstance(data, dict):
            return data

        legacy_to_core = {
            "API_HOST": "api_host",
            "API_PORT": "api_port",
            "API_BASE_URL": "api_base_url",
            "CORS_ORIGINS": "cors_origins",
            "LOG_LEVEL": "log_level",
            "APP_VERSION": "app_version",
            "DATA_SAMPLES_DIR": "data_samples_dir",
            "DATA_SYNTHETIC_DIR": "data_synthetic_dir",
            "EQUITY_DATA_PATH": "equity_data_path",
        }

        core_updates: dict[str, object] = {}
        for legacy_key, core_key in legacy_to_core.items():
            if legacy_key in data and "core" not in data:
                core_updates[core_key] = data[legacy_key]

        if core_updates:
            data = dict(data)
            data["core"] = core_updates
        return data

    @model_validator(mode="after")
    def _validate_enabled_integrations(self):
        if self.db.enabled and not self.db.dsn:
            raise ValueError("Database is enabled but IRIDIUM_DB__DSN is not configured")
        if self.cache.enabled and not self.cache.redis_url:
            raise ValueError("Cache is enabled but IRIDIUM_CACHE__REDIS_URL is not configured")
        if self.twogis.enabled and not self.twogis.api_key:
            raise ValueError("2GIS is enabled but IRIDIUM_TWOGIS__API_KEY is not configured")
        if self.moovit.enabled and not self.moovit.api_key:
            raise ValueError("Moovit is enabled but IRIDIUM_MOOVIT__API_KEY is not configured")
        if self.telemetry.enabled:
            if not self.telemetry.traccar_host:
                raise ValueError("Telemetry is enabled but IRIDIUM_TELEMETRY__TRACCAR_HOST is not configured")
            if not self.telemetry.traccar_user or not self.telemetry.traccar_password:
                raise ValueError("Telemetry is enabled but Traccar credentials are not configured")
        if self.yandex.enabled is False and self.transit.yandex_observed_enabled:
            raise ValueError("Transit requires Yandex observed but IRIDIUM_YANDEX__ENABLED is false")
        return self

    # Backward compatible aliases for existing code and tests
    @property
    def API_HOST(self) -> str:  # noqa: N802
        return self.core.api_host

    @property
    def API_PORT(self) -> int:  # noqa: N802
        return self.core.api_port

    @property
    def API_BASE_URL(self) -> str:  # noqa: N802
        return self.core.api_base_url

    @property
    def CORS_ORIGINS(self) -> str:  # noqa: N802
        return self.core.cors_origins

    @property
    def LOG_LEVEL(self) -> str:  # noqa: N802
        return self.core.log_level

    @property
    def DATA_SAMPLES_DIR(self) -> str:  # noqa: N802
        return self.core.data_samples_dir

    @property
    def DATA_SYNTHETIC_DIR(self) -> str:  # noqa: N802
        return self.core.data_synthetic_dir

    @property
    def EQUITY_DATA_PATH(self) -> str:  # noqa: N802
        return self.core.equity_data_path

    @property
    def APP_VERSION(self) -> str:  # noqa: N802
        return self.core.app_version

    def cors_origins_list(self) -> list[str]:
        return self.core.cors_origins_list()

    def data_samples_path(self) -> Path:
        return self.core.data_samples_path()

    def data_synthetic_path(self) -> Path:
        return self.core.data_synthetic_path()

    def equity_data_path(self) -> Optional[Path]:
        return self.core.equity_path()


def _secret_from_env(key: str) -> Optional[SecretStr]:
    v = os.getenv(key)
    return SecretStr(v) if v else None


@lru_cache
def get_settings() -> Settings:
    s = Settings()

    # Backward compatible env vars (for local dev files that predate IRIDIUM_ prefix).
    legacy_core = {
        "API_HOST": "api_host",
        "API_PORT": "api_port",
        "API_BASE_URL": "api_base_url",
        "CORS_ORIGINS": "cors_origins",
        "LOG_LEVEL": "log_level",
        "APP_VERSION": "app_version",
        "DATA_SAMPLES_DIR": "data_samples_dir",
        "DATA_SYNTHETIC_DIR": "data_synthetic_dir",
        "EQUITY_DATA_PATH": "equity_data_path",
    }

    updates: dict[str, object] = {}
    for legacy_key, core_key in legacy_core.items():
        v = os.getenv(legacy_key)
        if v is not None and v != "":
            updates[core_key] = v

    if updates:
        s = s.model_copy(update={"core": s.core.model_copy(update=updates)})

    # Legacy provider credentials: if IRIDIUM_* not set, fall back to TWOGIS_API_KEY, MOOVIT_*, etc.
    twogis_key = s.twogis.api_key or _secret_from_env("TWOGIS_API_KEY")
    if twogis_key is not None:
        s = s.model_copy(update={"twogis": s.twogis.model_copy(update={"api_key": twogis_key})})

    moovit_key = s.moovit.api_key or _secret_from_env("MOOVIT_API_KEY")
    moovit_url = s.moovit.base_url or os.getenv("MOOVIT_BASE_URL") or ""
    if moovit_key is not None or moovit_url:
        s = s.model_copy(update={
            "moovit": s.moovit.model_copy(update={
                "api_key": moovit_key or s.moovit.api_key,
                "base_url": moovit_url or s.moovit.base_url,
            })
        })

    eo_updates: dict[str, object] = {}
    if not s.eo.sentinel_hub_client_id:
        eo_updates["sentinel_hub_client_id"] = _secret_from_env("SENTINEL_HUB_CLIENT_ID") or s.eo.sentinel_hub_client_id
    if not s.eo.sentinel_hub_client_secret:
        eo_updates["sentinel_hub_client_secret"] = _secret_from_env("SENTINEL_HUB_CLIENT_SECRET") or s.eo.sentinel_hub_client_secret
    if not s.eo.cdse_username:
        eo_updates["cdse_username"] = _secret_from_env("CDSE_USERNAME") or s.eo.cdse_username
    if not s.eo.cdse_password:
        eo_updates["cdse_password"] = _secret_from_env("CDSE_PASSWORD") or s.eo.cdse_password
    if not s.eo.cdse_client_id:
        eo_updates["cdse_client_id"] = _secret_from_env("CDSE_CLIENT_ID") or s.eo.cdse_client_id
    if not s.eo.cdse_client_secret:
        eo_updates["cdse_client_secret"] = _secret_from_env("CDSE_CLIENT_SECRET") or s.eo.cdse_client_secret
    if eo_updates:
        s = s.model_copy(update={"eo": s.eo.model_copy(update=eo_updates)})

    gomap_key = s.gomap.api_key or _secret_from_env("GOMAP_API_KEY")
    gomap_ip = s.gomap.allowed_server_ip or os.getenv("GOMAP_ALLOWED_SERVER_IP")
    if gomap_key is not None or gomap_ip:
        s = s.model_copy(update={
            "gomap": s.gomap.model_copy(update={
                "api_key": gomap_key or s.gomap.api_key,
                "allowed_server_ip": gomap_ip or s.gomap.allowed_server_ip,
            })
        })

    return s


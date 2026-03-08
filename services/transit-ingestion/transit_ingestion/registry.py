"""
Transit provider registry. No GTFS is used until a real feed is provided.
Status: live, permission_required, unavailable, disabled.
"""

from datetime import datetime, timezone
from typing import Optional

from iridium_schemas.provenance import ProviderRegistryEntry

PROVIDER_LIVE = "live"
PROVIDER_PERMISSION_REQUIRED = "permission_required"
PROVIDER_UNAVAILABLE = "unavailable"
PROVIDER_DISABLED = "disabled"


class ProviderStatus:
    """Result of transit provider lookup."""

    def __init__(
        self,
        provider_id: str,
        status: str,
        feed_url: Optional[str] = None,
        note: Optional[str] = None,
    ):
        self.provider_id = provider_id
        self.status = status
        self.feed_url = feed_url
        self.note = note

    def to_registry_entry(self) -> ProviderRegistryEntry:
        return ProviderRegistryEntry(
            provider_id=self.provider_id,
            name=self.provider_id,
            status=self.status,
            feed_url=self.feed_url,
            updated_at=datetime.now(timezone.utc),
            note=self.note,
        )


# Registry: BakuBus (AYNA), Baku Metro (official), alerts, Yandex observed, 2GIS, Moovit.
_DEFAULT_REGISTRY: list[ProviderStatus] = [
    ProviderStatus(
        "bakubus_ayna",
        PROVIDER_LIVE,
        feed_url="https://map-api.ayna.gov.az/api/bus/getBusList",
        note="Public AYNA API; getBusById is public undocumented. source_status=public_undocumented.",
    ),
    ProviderStatus(
        "bakumetro_official",
        PROVIDER_LIVE,
        feed_url=None,
        note="Official website; static network only. source_status=static_schedule_only. No machine-readable GTFS from operator.",
    ),
    ProviderStatus(
        "bakubus_official_alerts",
        PROVIDER_LIVE,
        feed_url="https://bakubus.az/az/news",
        note="Official BakuBus news/notifications. source_status=official_alerts_only.",
    ),
    ProviderStatus(
        "bakumetro_official_alerts",
        PROVIDER_LIVE,
        feed_url="https://metro.gov.az/az/news",
        note="Official Baku Metro service updates. source_status=official_alerts_only.",
    ),
    ProviderStatus(
        "yandex_transport_observed",
        PROVIDER_LIVE,
        feed_url="https://yandex.az/maps",
        note="Public web observed; stop-level predictions from Yandex Baku pages. source_status=public_web_observed. Not official GTFS Realtime.",
    ),
    ProviderStatus(
        "yandex_metro_operational",
        PROVIDER_LIVE,
        feed_url="https://yandex.az/maps/10335/baku/metro/",
        note="Yandex Metro Baku operational context (closed stations, etc). source_status=public_web_operational_context.",
    ),
    ProviderStatus(
        "yandex_traffic_context",
        PROVIDER_LIVE,
        feed_url=None,
        note="Traffic context: web_observed or licensed_api when key set. Status from get_traffic_context_status.",
    ),
    ProviderStatus(
        "twogis_public_transport",
        PROVIDER_LIVE,
        feed_url="https://routing.api.2gis.com/public_transport/1.0",
        note="2GIS Public Transport API. source_status=licensed_partner. Requires TWOGIS_API_KEY.",
    ),
    ProviderStatus(
        "moovit_partner",
        PROVIDER_PERMISSION_REQUIRED,
        feed_url=None,
        note="Moovit partner. source_status=partner_required. Interface only until credentials configured.",
    ),
    ProviderStatus(
        "baku_metro",
        PROVIDER_PERMISSION_REQUIRED,
        feed_url=None,
        note="Operator GTFS not yet provided. Static model from bakumetro_official used instead.",
    ),
    ProviderStatus(
        "bakubus",
        PROVIDER_PERMISSION_REQUIRED,
        feed_url=None,
        note="Operator GTFS not yet provided. AYNA public API (bakubus_ayna) used instead.",
    ),
]


def get_provider_registry() -> list[ProviderRegistryEntry]:
    """Return current transit provider registry. No synthetic feeds."""
    return [p.to_registry_entry() for p in _DEFAULT_REGISTRY]

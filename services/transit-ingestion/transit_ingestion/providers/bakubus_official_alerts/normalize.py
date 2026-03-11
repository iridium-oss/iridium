"""
Normalize BakuBus official page content into canonical Alert entities.
source_family: official_website. source_status: official_alerts_only.
"""

import hashlib

from iridium_schemas.transit import Alert, SourceFamily, SourceStatus

from transit_ingestion.providers.bakubus_official_alerts.fetcher import (
    PROVIDER_ID,
    FetchedPage,
    _extract_news_items,
)

SOURCE_FAMILY = SourceFamily.OFFICIAL_WEBSITE.value
SOURCE_STATUS = SourceStatus.OFFICIAL_ALERTS_ONLY.value


def normalize_bakubus_alerts(
    fetched: FetchedPage,
    max_items: int = 30,
) -> list[Alert]:
    """
    Convert fetched BakuBus news page into Alert list. Deduplication by alert_id.
    Does not fabricate; only uses extracted title, url, fetched_at.
    """
    if fetched.error or not fetched.html:
        return []
    items = _extract_news_items(fetched.html, fetched.url)
    alerts = []
    for i, item in enumerate(items[:max_items]):
        url = item.get("url") or ""
        title = (item.get("title") or "").strip()
        if not title:
            title = "BakuBus update"
        alert_id = hashlib.sha256(f"{PROVIDER_ID}:{url}:{title}".encode()).hexdigest()[:24]
        alerts.append(
            Alert(
                alert_id=alert_id,
                title=title,
                published_at=fetched.fetched_at,
                provider="bakubus",
                affected_mode="bus",
                affected_route_id=None,
                affected_station_id=None,
                alert_category="news",
                severity=None,
                effective_start=None,
                effective_end=None,
                source_url=url,
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                observed_at=fetched.fetched_at,
                fetched_at=fetched.fetched_at,
                confidence="extracted_from_official_page",
                validation_note="Parsed from official BakuBus news page; structure may change.",
            )
        )
    return alerts


def fetch_bakubus_alerts(timeout: float = 20.0) -> list[Alert]:
    """Fetch and normalize BakuBus official alerts in one call."""
    from transit_ingestion.providers.bakubus_official_alerts.fetcher import (
        fetch_bakubus_news_page,
    )

    page = fetch_bakubus_news_page(timeout=timeout)
    return normalize_bakubus_alerts(page)

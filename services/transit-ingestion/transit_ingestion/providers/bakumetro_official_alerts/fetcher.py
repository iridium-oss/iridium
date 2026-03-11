"""
Fetch Baku Metro official news/service updates page. No fabricated data.
"""

import re
from dataclasses import dataclass
from datetime import UTC, datetime

import httpx

PROVIDER_ID = "bakumetro_official_alerts"
METRO_BASE = "https://metro.gov.az"
METRO_NEWS_URL = "https://metro.gov.az/az/news"
DEFAULT_TIMEOUT = 20.0
USER_AGENT = "IRIDIUM-transit-ingestion/0.1 (Baku Metro official alerts)"


@dataclass
class FetchedMetroPage:
    url: str
    html: str
    fetched_at: datetime
    status_code: int
    error: str | None = None


def fetch_metro_news_page(
    url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> FetchedMetroPage:
    """Fetch official Baku Metro news/updates page. Returns raw HTML and provenance."""
    target = url or METRO_NEWS_URL
    fetched_at = datetime.now(UTC)
    try:
        r = httpx.get(
            target,
            timeout=timeout,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        )
        r.raise_for_status()
        return FetchedMetroPage(
            url=target,
            html=r.text,
            fetched_at=fetched_at,
            status_code=r.status_code,
        )
    except httpx.HTTPStatusError as e:  # pragma: no cover
        return FetchedMetroPage(
            url=target,
            html="",
            fetched_at=fetched_at,
            status_code=e.response.status_code,
            error=str(e),
        )
    except Exception as e:  # pragma: no cover
        return FetchedMetroPage(
            url=target,
            html="",
            fetched_at=fetched_at,
            status_code=-1,
            error=str(e),
        )


def _extract_news_items(html: str, base_url: str) -> list[dict]:
    """Extract candidate news/update items from HTML. No fabrication."""
    items = []
    if not html or not html.strip():
        return items
    link_pattern = re.compile(
        r'<a\s+href="([^"]+)"[^>]*>([^<]*)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    for m in link_pattern.finditer(html):
        href = m.group(1).strip()
        text = m.group(2).strip()
        if not text or len(text) < 2:
            continue
        text = re.sub(r"\s+", " ", text)[:500]
        if href.startswith("#") or href.startswith("javascript:"):
            continue
        if not href.startswith("http"):
            from urllib.parse import urljoin

            href = urljoin(base_url, href)
        items.append({"url": href, "title": text})
    seen = set()
    out = []
    for x in items:
        if x["url"] in seen:
            continue
        seen.add(x["url"])
        out.append(x)
    return out[:50]

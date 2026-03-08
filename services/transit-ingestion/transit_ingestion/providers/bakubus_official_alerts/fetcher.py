"""
Fetch BakuBus official news/notifications page. No fabricated data.
"""

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import httpx

PROVIDER_ID = "bakubus_official_alerts"
# Official BakuBus site; adjust path if the site structure changes.
BAKUBUS_NEWS_URL = "https://bakubus.az"
BAKUBUS_NEWS_PAGE_URL = "https://bakubus.az/az/news"
DEFAULT_TIMEOUT = 20.0
USER_AGENT = "IRIDIUM-transit-ingestion/0.1 (BakuBus official alerts)"


@dataclass
class FetchedPage:
    url: str
    html: str
    fetched_at: datetime
    status_code: int
    error: Optional[str] = None


def fetch_bakubus_news_page(
    url: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> FetchedPage:
    """Fetch official BakuBus news/notifications page. Returns raw HTML and provenance."""
    target = url or BAKUBUS_NEWS_PAGE_URL
    fetched_at = datetime.now(timezone.utc)
    try:
        r = httpx.get(
            target,
            timeout=timeout,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        )
        r.raise_for_status()
        html = r.text
        return FetchedPage(
            url=target,
            html=html,
            fetched_at=fetched_at,
            status_code=r.status_code,
        )
    except httpx.HTTPStatusError as e:
        return FetchedPage(
            url=target,
            html="",
            fetched_at=fetched_at,
            status_code=e.response.status_code,
            error=str(e),
        )
    except Exception as e:
        return FetchedPage(
            url=target,
            html="",
            fetched_at=fetched_at,
            status_code=-1,
            error=str(e),
        )


def _extract_news_items(html: str, base_url: str) -> list[dict]:
    """Extract candidate news items from HTML. Structure depends on live site; no fabrication."""
    items = []
    if not html or not html.strip():
        return items
    # Common patterns: links with href and text, optional date-like text nearby.
    # Match <a href="...">...</a> and capture href and inner text.
    link_pattern = re.compile(
        r'<a\s+href="([^"]+)"[^>]*>([^<]*)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    for m in link_pattern.finditer(html):
        href = m.group(1).strip()
        text = m.group(2).strip()
        if not text or len(text) < 3:
            continue
        text = re.sub(r"\s+", " ", text)[:500]
        if href.startswith("#") or href.startswith("javascript:"):
            continue
        if not href.startswith("http"):
            from urllib.parse import urljoin
            href = urljoin(base_url, href)
        items.append({"url": href, "title": text})
    # Deduplicate by url
    seen = set()
    out = []
    for x in items:
        if x["url"] in seen:
            continue
        seen.add(x["url"])
        out.append(x)
    return out[:50]

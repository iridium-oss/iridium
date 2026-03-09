"""
Fetch Yandex Metro Baku page for operational context. Public web; not operator feed.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import httpx

PROVIDER_ID = "yandex_metro_operational"
YANDEX_METRO_BAKU = "https://yandex.az/maps/10335/baku/metro/"
DEFAULT_TIMEOUT = 15.0
USER_AGENT = "Mozilla/5.0 (compatible; IRIDIUM-transit/0.1; Baku metro operational)"


@dataclass
class FetchedMetroPage:
    url: str
    html: str
    fetched_at: datetime
    status_code: int
    error: Optional[str] = None


def fetch_yandex_metro_page(
    url: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> FetchedMetroPage:
    """Fetch Yandex Metro Baku page. Content may be JS-rendered."""
    target = url or YANDEX_METRO_BAKU
    fetched_at = datetime.now(timezone.utc)
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
    except Exception as e:  # pragma: no cover
        return FetchedMetroPage(
            url=target,
            html="",
            fetched_at=fetched_at,
            status_code=-1,
            error=str(e),
        )

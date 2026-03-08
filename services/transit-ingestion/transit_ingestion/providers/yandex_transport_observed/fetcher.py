"""
Fetch Yandex Baku public transport / stop pages. Public web only; not official operator feed.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import httpx

PROVIDER_ID = "yandex_transport_observed"
# Example: Yandex Maps Baku transport; stop pages vary by stop. Use a representative URL pattern.
YANDEX_BAKU_TRANSPORT_BASE = "https://yandex.az/maps"
DEFAULT_TIMEOUT = 15.0
USER_AGENT = "Mozilla/5.0 (compatible; IRIDIUM-transit/0.1; Baku transport observation)"


@dataclass
class FetchedYandexPage:
    url: str
    html: str
    fetched_at: datetime
    status_code: int
    error: Optional[str] = None


def fetch_yandex_stop_page(
    stop_url: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> FetchedYandexPage:
    """
    Fetch a Yandex Baku transport or stop page. Returns raw HTML.
    Page content may be JS-rendered; parser may get no structured data.
    """
    url = stop_url or YANDEX_BAKU_TRANSPORT_BASE
    fetched_at = datetime.now(timezone.utc)
    try:
        r = httpx.get(
            url,
            timeout=timeout,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        )
        r.raise_for_status()
        return FetchedYandexPage(
            url=url,
            html=r.text,
            fetched_at=fetched_at,
            status_code=r.status_code,
        )
    except httpx.HTTPStatusError as e:
        return FetchedYandexPage(
            url=url,
            html="",
            fetched_at=fetched_at,
            status_code=e.response.status_code,
            error=str(e),
        )
    except Exception as e:
        return FetchedYandexPage(
            url=url,
            html="",
            fetched_at=fetched_at,
            status_code=-1,
            error=str(e),
        )

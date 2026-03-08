"""
Normalize Yandex Metro Baku page to MetroOperationalNotice and MetroRoutingConstraint.
Public-web operational context only.
"""

import re
from datetime import datetime, timezone

from iridium_schemas.transit import (
    MetroOperationalNotice,
    MetroRoutingConstraint,
    SourceFamily,
    SourceStatus,
)

from transit_ingestion.providers.yandex_metro_operational.fetcher import (
    FetchedMetroPage,
    PROVIDER_ID,
)

SOURCE_FAMILY = SourceFamily.PUBLIC_WEB.value
SOURCE_STATUS = SourceStatus.PUBLIC_WEB_OPERATIONAL_CONTEXT.value


def _extract_closed_hints(html: str) -> list[dict]:
    """Extract hints of closed stations or entrances from HTML. No fabrication."""
    out = []
    # Common phrases in Russian/Azerbaijani/English for closed/restricted.
    for pattern in [
        r"closed\s+station",
        r"station\s+closed",
        r"entrance\s+closed",
        r"закрыт",
        r"закрыта",
        r"restricted",
    ]:
        for m in re.finditer(pattern, html, re.IGNORECASE):
            out.append({"type": "closed_or_restricted", "raw": m.group(0)})
    return out[:20]


def normalize_yandex_metro_operational(
    fetched: FetchedMetroPage,
) -> tuple[list[MetroOperationalNotice], list[MetroRoutingConstraint]]:
    """Normalize fetched page to operational notices and routing constraints."""
    notices: list[MetroOperationalNotice] = []
    constraints: list[MetroRoutingConstraint] = []
    if fetched.error or not fetched.html:
        return notices, constraints
    hints = _extract_closed_hints(fetched.html)
    for i, h in enumerate(hints):
        notice_id = f"{PROVIDER_ID}_notice_{i}_{int(fetched.fetched_at.timestamp())}"
        notices.append(
            MetroOperationalNotice(
                notice_id=notice_id,
                station_id=None,
                notice_type=h.get("type", "closed_or_restricted"),
                description=h.get("raw"),
                effective_start=None,
                effective_end=None,
                observed_at=fetched.fetched_at,
                source_provider=PROVIDER_ID,
                source_family=SOURCE_FAMILY,
                source_status=SOURCE_STATUS,
                source_url=fetched.url,
                confidence="public_web_observed",
                validation_note="Extracted from Yandex Metro page; may be incomplete if JS-rendered.",
            )
        )
    return notices, constraints

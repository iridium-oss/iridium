"""
AYNA map API client for BakuBus.
GET https://map-api.ayna.gov.az/api/bus/getBusList - public.
GET https://map-api.ayna.gov.az/api/bus/getBusById?id={id} - public undocumented.
Strong error handling, retry, timeout, rate limiting. Provenance on every fetch.
"""

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import httpx

AYNA_BUS_LIST_URL = "https://map-api.ayna.gov.az/api/bus/getBusList"
AYNA_BUS_BY_ID_URL = "https://map-api.ayna.gov.az/api/bus/getBusById"

DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 2
RETRY_BACKOFF = 1.0
MIN_REQUEST_INTERVAL = 0.5

CACHE_DIR_ENV = "IRIDIUM_TRANSIT_CACHE_DIR"
DEFAULT_CACHE_DIR = ".transit_cache"


@dataclass
class FetchResult:
    """Result of a single fetch with provenance."""

    data: Any
    source_url: str
    fetched_at: datetime
    response_status: int
    response_checksum: Optional[str] = None
    error: Optional[str] = None


def _checksum(data: Any) -> str:
    """Deterministic checksum of JSON-serializable data."""
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _cache_dir() -> Path:
    base = Path(os.environ.get(CACHE_DIR_ENV, DEFAULT_CACHE_DIR))
    if not base.is_absolute():
        base = Path.cwd() / base
    sub = base / "bakubus_ayna"
    sub.mkdir(parents=True, exist_ok=True)
    return sub


def _write_raw_cache(key: str, payload: Any, fetched_at: datetime) -> None:
    """Write raw response to cache (gitignored)."""
    try:
        d = _cache_dir()
        safe_key = key.replace("/", "_").replace("?", "_")[:120]
        ts = fetched_at.strftime("%Y%m%d_%H%M%S")
        path = d / f"{safe_key}_{ts}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=0)
    except Exception:  # pragma: no cover
        pass


def _rate_limit(last_request_time: list[float]) -> None:
    """Enforce minimum interval between requests."""
    now = time.monotonic()
    if last_request_time:
        elapsed = now - last_request_time[0]
        if elapsed < MIN_REQUEST_INTERVAL:
            time.sleep(MIN_REQUEST_INTERVAL - elapsed)
    last_request_time.clear()
    last_request_time.append(time.monotonic())


def fetch_bus_list(
    timeout: float = DEFAULT_TIMEOUT,
    cache_raw: bool = True,
    client: Optional[httpx.Client] = None,
    last_request_time: Optional[list[float]] = None,
) -> FetchResult:
    """
    Fetch route list from AYNA getBusList.
    Returns list of bus/route identifiers. Provenance recorded.
    """
    url = AYNA_BUS_LIST_URL
    fetched_at = datetime.now(timezone.utc)
    lrt = last_request_time if last_request_time is not None else []
    _rate_limit(lrt)

    status_code = -1
    last_err: Optional[Exception] = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            with client or httpx.Client(timeout=timeout) as c:
                r = c.get(url)
                status_code = r.status_code
                r.raise_for_status()
                data = r.json()
            last_err = None
            break
        except (httpx.TimeoutException, httpx.HTTPStatusError, OSError) as e:  # pragma: no cover
            last_err = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF)
            else:
                if isinstance(e, httpx.TimeoutException):
                    return FetchResult(  # pragma: no cover
                        data=[], source_url=url, fetched_at=fetched_at,
                        response_status=-1, error=f"timeout after {MAX_RETRIES + 1} attempts: {e}",
                    )
                if isinstance(e, httpx.HTTPStatusError):
                    return FetchResult(  # pragma: no cover
                        data=[], source_url=url, fetched_at=fetched_at,
                        response_status=e.response.status_code, error=str(e),
                    )
                return FetchResult(  # pragma: no cover
                    data=[], source_url=url, fetched_at=fetched_at,
                    response_status=-1, error=str(last_err),
                )
        except Exception as e:  # pragma: no cover
            last_err = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF)
            else:
                return FetchResult(  # pragma: no cover
                    data=[], source_url=url, fetched_at=fetched_at,
                    response_status=-1, error=str(e),
                )
    if last_err is not None:  # pragma: no cover
        return FetchResult(
            data=[], source_url=url, fetched_at=fetched_at,
            response_status=-1, error=str(last_err),
        )
    checksum = _checksum(data)
    if cache_raw:
        _write_raw_cache("getBusList", data, fetched_at)

    return FetchResult(
        data=data,
        source_url=url,
        fetched_at=fetched_at,
        response_status=status_code,
        response_checksum=checksum,
    )


def fetch_bus_by_id(
    bus_id: str,
    timeout: float = DEFAULT_TIMEOUT,
    cache_raw: bool = True,
    client: Optional[httpx.Client] = None,
    last_request_time: Optional[list[float]] = None,
) -> FetchResult:
    """
    Fetch route detail from AYNA getBusById.
    Public undocumented endpoint. Provenance recorded.
    """
    url = f"{AYNA_BUS_BY_ID_URL}?id={bus_id}"
    fetched_at = datetime.now(timezone.utc)
    lrt = last_request_time if last_request_time is not None else []
    _rate_limit(lrt)

    status_code = -1
    data = None
    last_err_id: Optional[Exception] = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            with client or httpx.Client(timeout=timeout) as c:
                r = c.get(url)
                status_code = r.status_code
                r.raise_for_status()
                data = r.json()
            last_err_id = None
            break
        except (httpx.TimeoutException, httpx.HTTPStatusError, OSError) as e:  # pragma: no cover
            last_err_id = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF)
            else:
                if isinstance(e, httpx.TimeoutException):
                    return FetchResult(  # pragma: no cover
                        data=None, source_url=url, fetched_at=fetched_at,
                        response_status=-1, error=f"timeout after {MAX_RETRIES + 1} attempts: {e}",
                    )
                if isinstance(e, httpx.HTTPStatusError):
                    return FetchResult(  # pragma: no cover
                        data=None, source_url=url, fetched_at=fetched_at,
                        response_status=e.response.status_code, error=str(e),
                    )
                return FetchResult(  # pragma: no cover
                    data=None, source_url=url, fetched_at=fetched_at,
                    response_status=-1, error=str(last_err_id),
                )
        except Exception as e:  # pragma: no cover
            last_err_id = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF)
            else:
                return FetchResult(  # pragma: no cover
                    data=None, source_url=url, fetched_at=fetched_at,
                    response_status=-1, error=str(e),
                )
    if last_err_id is not None or data is None:  # pragma: no cover
        return FetchResult(
            data=None, source_url=url, fetched_at=fetched_at,
            response_status=status_code, error=str(last_err_id or "no data"),
        )
    checksum = _checksum(data)
    if cache_raw:
        _write_raw_cache(f"getBusById_{bus_id}", data, fetched_at)
    return FetchResult(
        data=data,
        source_url=url,
        fetched_at=fetched_at,
        response_status=status_code,
        response_checksum=checksum,
    )

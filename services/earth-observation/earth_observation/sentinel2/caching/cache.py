"""
In-memory cache for EO search results and layer descriptors.
TTL-based; no Redis dependency. Optional file-backed cache can be added via config.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Optional

from iridium_schemas.earth_observation import EOSceneSearchResult

_CACHE: dict[str, tuple[Any, float]] = {}
_DEFAULT_TTL_SECONDS = 300  # 5 minutes for search
_LAYER_TTL_SECONDS = 600  # 10 minutes for layer descriptors


def _cache_key(prefix: str, *parts: Any) -> str:
    raw = json.dumps(parts, sort_keys=True, default=str)
    return f"{prefix}:{hashlib.sha256(raw.encode()).hexdigest()[:24]}"


def get_cached_search(key_parts: tuple[Any, ...], ttl: int = _DEFAULT_TTL_SECONDS) -> Optional[EOSceneSearchResult]:
    """Return cached EOSceneSearchResult if present and not expired."""
    k = _cache_key("eo_search", key_parts)
    if k not in _CACHE:
        return None
    data, expires = _CACHE[k]
    if time.time() > expires:
        del _CACHE[k]
        return None
    return data


def set_cached_search(key_parts: tuple[Any, ...], result: EOSceneSearchResult, ttl: int = _DEFAULT_TTL_SECONDS) -> None:
    """Store search result in cache."""
    k = _cache_key("eo_search", key_parts)
    _CACHE[k] = (result, time.time() + ttl)


def get_cached_layer_descriptor(key_parts: tuple[Any, ...], ttl: int = _LAYER_TTL_SECONDS) -> Optional[dict[str, Any]]:
    """Return cached layer descriptor dict if present and not expired."""
    k = _cache_key("eo_layer", key_parts)
    if k not in _CACHE:
        return None
    data, expires = _CACHE[k]
    if time.time() > expires:
        del _CACHE[k]
        return None
    return data


def set_cached_layer_descriptor(
    key_parts: tuple[Any, ...], descriptor: dict[str, Any], ttl: int = _LAYER_TTL_SECONDS
) -> None:
    """Store layer descriptor in cache."""
    k = _cache_key("eo_layer", key_parts)
    _CACHE[k] = (descriptor, time.time() + ttl)

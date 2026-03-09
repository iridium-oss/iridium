"""
Log redaction utilities.

The goal is to prevent accidental leakage of credentials and tokens in structured logs.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


REDACTED = "[REDACTED]"

SENSITIVE_KEY_PARTS = {
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "cookie",
    "set-cookie",
    "dsn",
    "redis_url",
    "postgres_password",
    "traccar_password",
    "traffic_api_key",
}


def _is_sensitive_key(key: str) -> bool:
    k = (key or "").strip().lower().replace("-", "_")
    return any(part in k for part in SENSITIVE_KEY_PARTS)


def redact_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: (REDACTED if _is_sensitive_key(str(k)) else redact_value(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_value(v) for v in value]
    if isinstance(value, tuple):
        return tuple(redact_value(v) for v in value)
    return value


def redact_event_dict(event_dict: dict[str, Any]) -> dict[str, Any]:
    return {k: (REDACTED if _is_sensitive_key(k) else redact_value(v)) for k, v in event_dict.items()}


"""
Structured logging configuration for the API service.
"""

from __future__ import annotations

import logging
import sys

import structlog
from app.observability.redaction import redact_event_dict


def configure_logging(log_level: str = "INFO") -> None:
    """
    Configure stdlib logging and structlog.

    This function is safe to call multiple times.
    """
    level = getattr(logging, (log_level or "INFO").upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(message)s",
        stream=sys.stdout,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            lambda _, __, event_dict: redact_event_dict(event_dict),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None):
    return structlog.get_logger(name)

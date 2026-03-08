"""
Transit storage: cache directory for raw payloads (gitignored), feed export directory for GTFS.
"""

import os
from pathlib import Path

FEED_EXPORT_DIR_ENV = "IRIDIUM_GTFS_OUTPUT_DIR"
DEFAULT_FEED_EXPORT_DIR = "feed_export"


def get_feed_export_dir() -> Path:
    """Return the feed export directory for GTFS and OTP preparation. Creates dir if missing."""
    raw = os.environ.get(FEED_EXPORT_DIR_ENV, DEFAULT_FEED_EXPORT_DIR)
    path = Path(raw)
    if not path.is_absolute():
        path = Path.cwd() / path
    path.mkdir(parents=True, exist_ok=True)
    return path

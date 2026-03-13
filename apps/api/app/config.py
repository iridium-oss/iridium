"""
Backward compatible settings module.

New code should import settings from app.core.settings.
"""

from app.core.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]

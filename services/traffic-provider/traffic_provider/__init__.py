"""
Traffic provider abstraction. When credentials are present, use real provider (e.g. TomTom).
When absent, return configuration_required; no synthetic traffic.
"""

from traffic_provider.provider import get_traffic_status, get_segment_speeds

__all__ = ["get_traffic_status", "get_segment_speeds"]

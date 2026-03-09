"""
Dataset loading for federated clients.

Each client loads only its partition; no central raw data merge.
"""

from .loader import load_client_data

__all__ = ["load_client_data"]

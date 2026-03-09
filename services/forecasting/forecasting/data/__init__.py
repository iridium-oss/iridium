"""
Dataset builder for forecasting. Time-aligned data from network, weather, transit.
Manifests record coverage, time span, geography, missingness, and freshness.
"""

from .builder import build_forecast_dataset, DatasetManifest
from .sources import snapshot_to_observations

__all__ = ["build_forecast_dataset", "DatasetManifest", "snapshot_to_observations"]

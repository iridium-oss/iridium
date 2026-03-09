"""
Simple baselines for sanity checking and fallback. First-class evaluation.
"""

from .persistence import persistence_forecast
from .rolling import rolling_mean_forecast
from .linear import linear_temporal_forecast

__all__ = ["persistence_forecast", "rolling_mean_forecast", "linear_temporal_forecast"]

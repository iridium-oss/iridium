"""
Graph construction for forecasting. Builds adjacency and support matrices from network topology.
"""

from .builder import ForecastGraphMetadata, build_forecast_graph

__all__ = ["build_forecast_graph", "ForecastGraphMetadata"]

"""
Graph construction for forecasting. Builds adjacency and support matrices from network topology.
"""

from .builder import build_forecast_graph, ForecastGraphMetadata

__all__ = ["build_forecast_graph", "ForecastGraphMetadata"]

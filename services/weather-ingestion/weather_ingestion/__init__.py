"""
Real weather ingestion from Open-Meteo. No synthetic weather in main path.
"""

from weather_ingestion.open_meteo import fetch_weather, WeatherResult

__all__ = ["fetch_weather", "WeatherResult"]

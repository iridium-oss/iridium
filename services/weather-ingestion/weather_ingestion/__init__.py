"""
Real weather ingestion from Open-Meteo. No synthetic weather in main path.
"""

from weather_ingestion.open_meteo import WeatherResult, fetch_weather

__all__ = ["fetch_weather", "WeatherResult"]

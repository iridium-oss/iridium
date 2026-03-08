# Weather Integration

IRIDIUM uses real meteorological data for Baku and Quba. The primary operational source is Open-Meteo.

## Source

- **Open-Meteo**: https://open-meteo.com. Free API for forecast and historical weather. No API key required for basic usage; rate limits apply. Attribution required.
- **License**: See https://open-meteo.com/en/terms. Use in accordance with terms.

## Implementation

- **Service**: services/weather-ingestion. Fetches current and forecast weather for configured locations (Baku, Quba).
- **Location mapping**: Baku (lat 40.4093, lon 49.8671), Quba (lat 41.3617, lon 48.5136). Configurable via WEATHER_LOCATIONS or config file.
- **Cadence**: Configurable (e.g. hourly). Pipeline records fetched_at and source in provenance.
- **Storage**: Observations stored with source_type weather; observed_at and payload. Used as contextual features for forecasting and digital twin; not personal data.

## Fallback

There is no synthetic weather in the main application path. If the Open-Meteo request fails, the weather layer returns unavailable and the application exposes that status. No fabricated weather values.

## Provenance

Each weather observation or snapshot includes:
- source: open_meteo
- fetched_at: timestamp
- location_id: Baku or Quba (or configured id)

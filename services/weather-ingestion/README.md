# Weather Ingestion

Real weather data from Open-Meteo for Baku and Quba. No synthetic weather in the main path.

## Source

- Open-Meteo (https://open-meteo.com). Free API; attribution required. See docs/weather-integration.md and docs/source-licensing.md.

## Usage

- `fetch_weather()` returns WeatherResult with snapshots and status (live or unavailable). On API failure, status is unavailable and snapshots are empty; no fabricated values.
- Provenance is attached for API and digital twin state assembler.

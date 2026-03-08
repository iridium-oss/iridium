# Energy Context

IRIDIUM may use real energy context data as exogenous features (e.g. for future electric mobility or grid-aware analytics). No synthetic energy signals are used in the main runtime path.

## Candidate Sources

- Official national open data (Azerbaijan) where available and licensing permits.
- Public electricity balance or grid datasets.
- Azerbaijan power plant and transmission network datasets where terms permit.
- Open infrastructure mapping as supplementary context only.

## Use

- **Role**: Low-frequency energy context (e.g. regional or national) as exogenous features only. Not used as fake direct causation for traffic or demand.
- **Service**: services/energy-context. When configured and source is available, pipeline fetches and normalises; otherwise returns unavailable.
- **Data quality**: Document spatial accuracy and quality notes. Use conservatively.

## Status

When no real source is configured or licensed, energy context layer returns unavailable. No synthetic energy signal generation in main path.

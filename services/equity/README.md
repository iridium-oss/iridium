# Equity Service

Mobility Equity Score: district-level indicators to support identification of accessibility gaps and data-driven prioritisation. Baseline implementation uses synthetic or file-based district metrics. Policy use should consider documented assumptions and bias risks.

## Implemented

- get_equity_scores(district_ids, data_dir) returns MobilityEquityScore.
- Indicators: average travel time to services, PT accessibility proxy, modal availability proxy, affordability proxy, composite score.
- Default synthetic districts when no data file is present.

## Limitations

- Data coverage and indicator choice can introduce bias; see docs/fairness.md and research/risks-and-limitations.md.
- Composite formula is simple average; weighting is configurable in future.

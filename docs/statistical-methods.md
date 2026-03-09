# Statistical Methods

This document describes the statistical foundations used in IRIDIUM: descriptive statistics, missing data, outlier handling, and how they apply to each subsystem. All statistics are real, interpretable, and tied to product functions.

## Descriptive Statistics

- **Equity**: District-level proxies (pt_accessibility_proxy, modal_availability_proxy, affordability_proxy) are averaged into a composite: (pt + modal + aff) / 3. Raw values are taken from file-based input; no synthetic defaults in the main path.
- **Forecast**: Baseline uses no distributional statistics; it uses a fixed decay and edge attributes. Future time-series baselines may use rolling mean and variance.
- **Anomaly**: Rule-based thresholds (e.g. occupancy > 85%); no z-score or distribution fit in production yet.

## Missing Data

- **Policy**: No active AI endpoint uses synthetic runtime data to fill gaps. Missing data results in unavailable or reduced coverage and is reported via data_status and notes.
- **Equity**: When no data path is configured, districts list is empty and data_status is unavailable.
- **Forecast**: When twin has no edges, baseline still runs with default constants; source_coverage reflects "twin_edges=0" and confidence_note states limitations.
- **Routing**: When graph is empty, response has no alternatives or an explicit fallback with fallback_used True.

## Outlier Handling

- **Anomaly**: High occupancy (> 85%) is treated as demand_surge; incident flag is taken as given. No robust z-score or MAD in production baseline.
- **Equity**: Proxies are used as provided; no automatic winsorization. Documented in [fairness.md](fairness.md) and in the equity note (derived index; not official policy).

## Uncertainty and Intervals

- **Forecast baseline**: No confidence intervals or uncertainty bands; confidence_note explains this.
- **Equity**: No interval estimation; confidence_note states to interpret with caution when coverage is partial.
- Bootstrap or Bayesian summaries are not implemented unless explicitly added and documented.

## Temporal and Rolling Logic

- **Forecast**: Step-wise projection over horizon (e.g. 15 min steps); no rolling window over historical series in baseline.
- **Anomaly**: Optional since parameter to filter by detected_at; no rolling baseline deviation in production yet.

## Calibration and Evaluation

Where a learned model is introduced, calibration and evaluation will be documented in the evaluation plan. Current baselines are not calibrated; they are deterministic or rule-based.

All statistics are documented here and in subsystem docs. No false precision or unsupported claims.

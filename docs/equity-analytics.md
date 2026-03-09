# Equity Analytics

This document describes the Mobility Equity Score module: formulation, data source, limitations, and how it is exposed. It matches the implemented system and [fairness.md](fairness.md).

## Formulation

District-level composite score:

- **Input**: Per-district proxies from file-based data (district_scores.json): pt_accessibility_proxy, modal_availability_proxy, affordability_proxy. Each in [0, 1] or normalized.
- **Formula**: composite_score = (pt_accessibility_proxy + modal_availability_proxy + affordability_proxy) / 3. Implemented in `equity/score.py`.
- **Output**: DistrictScore per district with district_id, optional district_name, composite_score, and the three proxies. Response includes model_type, model_maturity, source_coverage, confidence_note, data_status, and note.

## Data Source

Real or recorded data only. The path is set via EQUITY_DATA_PATH to a directory containing district_scores.json. When the path is missing or the file is absent, the API returns empty districts and data_status unavailable with a clear note. No synthetic default in the main path.

## Bias and Limitation Notes

- The note states: "Derived analytic index; not an official government measurement. See docs/fairness.md."
- When data is incomplete, confidence_note states that the composite is from file-based proxies and should be interpreted with caution when coverage is partial.
- Data coverage bias and indicator choice limitations are documented in [fairness.md](fairness.md). The module does not present the score as official public policy truth.

## Normalization

Proxies are used as provided from the file. No z-score normalization across districts is applied in the current implementation; the formula is a simple average of three proxies. If raw values are not in [0, 1], the implementation uses defaults (0.5) only when the key is missing, not for out-of-range values (caller must ensure valid input).

## API and Metadata

Every response includes data_status, note, model_type, model_maturity, source_coverage, and confidence_note so that consumers can judge reliability and scope.

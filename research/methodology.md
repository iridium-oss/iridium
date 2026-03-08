# Methodology

This document outlines the methodology for the IRIDIUM project: design choices, data and model assumptions, and how the four core modules are developed and validated. It is intended to support reproducibility and critical review.

## Current Baseline

The repository implements a runnable baseline: in-memory digital twin, heuristic congestion forecast, baseline multimodal routing, district-level Mobility Equity Score from synthetic or file data, and rule-based anomaly detection. Federated learning and ST-GNN forecasting are not yet implemented; the methodology below applies to the baseline and to future extensions.

## Overall Approach

IRIDIUM follows an engineering and research methodology that combines:

- **System design**: Architecture and data contracts are designed first; implementation follows with documentation in lockstep.
- **Federated learning**: Training methodology (local update, aggregation, encryption or secure aggregation) is documented with assumptions and threat model. Evaluation considers both model quality and privacy-related properties where applicable.
- **Modular development**: Forecasting, routing, equity, and anomaly modules have defined interfaces and data dependencies. Each can be developed and tested with synthetic or partial real data before full integration.
- **Documentation of limitations**: Assumptions, data coverage, and bias risks are documented in the repository and in research docs so that results are interpretable.

## Data

- **Sources**: As per [docs/data-sources.md](../docs/data-sources.md). Data contracts define schemas; ingestion pipelines validate and normalise. No raw personal data in central or shared stores.
- **Splits**: For forecasting and anomaly detection, temporal splits (e.g. train on past, test on future) are used to avoid leakage. Spatial or participant-level splits may be used for federated evaluation.
- **Synthetic data**: Where real data is unavailable or restricted, synthetic or public benchmark data may be used for development and validation. This will be clearly stated in evaluation reports.

## Models

- **Forecasting**: ST-GNN or equivalent over graph $G = (V, E)$ with input $X_{t-T+1:t}$ and forecast $\hat{Y}_{t+1:t+H}$; loss such as MAE or RMSE. Baseline models (persistence, historical average) are used for comparison. See [docs/modeling.md](../docs/modeling.md).
- **Routing**: Optimization formulation (objectives, constraints) and graph construction are documented. Validation via comparison to known shortest paths or to external routing engines where applicable.
- **Equity**: Indicator definitions, formulas, and data requirements are documented. Validation includes sensitivity to indicator choice and to data coverage. See [docs/fairness.md](../docs/fairness.md).
- **Anomaly detection**: Detection rules or models and thresholds are documented. Validation includes precision/recall on labelled incidents where available; otherwise qualitative review and operational feedback.

## Evaluation

Evaluation plan, metrics, and reporting are detailed in [evaluation-plan.md](evaluation-plan.md). Reproducibility requires versioned code, configs, and data references (or synthetic data description).

## Revisions

Methodology may be revised as the project evolves. Significant changes will be recorded in this document and, when appropriate, in the CHANGELOG and release notes.

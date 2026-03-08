# Mobility Equity Score

This document describes the Mobility Equity Score in IRIDIUM: its objective, possible indicators, district-level comparison, accessibility gaps, policy relevance, and limitations and bias risks.

## Objective

The Mobility Equity Score aims to support identification of spatial accessibility gaps and data-driven infrastructure prioritisation. It is a set of district-level (or zone-level) indicators that summarise how well different areas are served by the transport network and by the prediction and routing services. The goal is to inform policy discussion and prioritisation, not to make automatic decisions.

## Score Formulation

District-level indicators are normalised (e.g. z-score) and combined into a composite Mobility Equity Score. For district $d$ and indicators $m = 1, \ldots, M$:

$$
z_{d,m} = \frac{x_{d,m} - \mu_m}{\sigma_m}, \qquad MES_d = \sum_{m=1}^{M} w_m \, z_{d,m}
$$

where $x_{d,m}$ is the raw value, $\mu_m$ and $\sigma_m$ the mean and standard deviation over districts, and $w_m$ non-negative weights. $MES_d$ is a derived analytic index produced by the platform; it is not an official government measurement. See [docs/symbol-glossary.md](symbol-glossary.md).

## Possible Indicators

- **Accessibility to key destinations**: Count or weighted sum of jobs, healthcare, or education reachable within a time or cost threshold from the district (e.g. 30 or 45 minutes by public transport).
- **Service level**: Frequency or capacity of public transport in the district; share of population within walking distance of a stop.
- **Predicted congestion or delay**: Average forecasted delay or congestion level for the district, as a proxy for reliability.
- **Routing outcome parity**: Comparison of average journey time or cost from the district to a common destination (e.g. city centre) versus other districts. Disparities may indicate underserved areas.

Indicators will be defined precisely (formulas, data sources, units) in the implementation and in the evaluation plan. Default choices may not suit all cities; they should be configurable or extensible.

## District-Level Comparison

Scores or indicators are computed per district (or zone). Districts are defined by administrative boundaries or by a standard grid. Comparison across districts highlights:

- Which areas have low accessibility or high congestion relative to others.
- Temporal changes (e.g. improvement after a new line) when historical data is available.

Aggregation (e.g. city-wide average) can hide local gaps; district-level granularity is therefore central.

## Accessibility Gaps

An accessibility gap is a shortfall in service or outcome for a district relative to a reference (e.g. city average or policy target). The Mobility Equity Score module is intended to surface such gaps so that planners can prioritise interventions. It does not by itself define what is "fair"; that is a policy and normative question. The module provides data and visualisation to support that discussion.

## Policy Relevance

Outputs are designed to be usable by transport authorities and planners for:

- Prioritising infrastructure investment or service changes.
- Monitoring progress toward equity or accessibility targets.
- Communicating spatial disparities to stakeholders.

The project does not prescribe policy; it provides tools that can support evidence-based debate.

## Limitations and Bias Risks

- **Data coverage bias**: If sensors or telemetry under-cover certain areas (e.g. informal settlements, peripheral districts), indicators will be biased. Gaps in data should be reported explicitly (e.g. "no data" or "low confidence").
- **Indicator choice**: The choice of indicators and weights is value-laden. Different choices can change which areas appear most disadvantaged. Documentation and configurability are important.
- **Causation**: Correlation between low scores and poor outcomes does not alone imply causation. Policy use should consider confounding factors and external validation.
- **Representation**: District-level aggregation can hide within-district inequality (e.g. by income or demographic). Finer granularity or subgroup analysis may be added in future but is not guaranteed.

These limitations are documented so that users and reviewers can interpret the Mobility Equity Score appropriately. Bias and fairness are discussed further in [research/risks-and-limitations.md](../research/risks-and-limitations.md).

## Current Implementation

The equity service computes composite scores from district-level proxies (e.g. PT accessibility, modal availability, affordability). The baseline uses synthetic or file-based district data; no claim is made about accuracy or policy readiness. Outputs are suitable for demonstration and for informing further indicator design and validation work.

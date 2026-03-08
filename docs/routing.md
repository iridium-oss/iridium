# Multimodal Adaptive Routing

This document describes the multimodal adaptive routing objective and candidate optimization criteria for IRIDIUM.

## Objective

The routing module computes journeys across multiple modes: bus, metro, minibus, walking, and cycling. Routes are adaptive in the sense that they use the current (or forecast) state of the digital twin, so that travel times and availability reflect real-time conditions. The objective is to support user or operator preferences over time, cost, and environmental impact while respecting constraints (e.g. transfer limits, accessibility).

## Route Utility

The routing module optimises a weighted objective over a route $r$:

$$
J(r) = \alpha \, T(r) + \beta \, C(r) + \gamma \, E(r) + \delta \, P(r)
$$

where $T(r)$ is travel time, $C(r)$ monetary or generalised cost, $E(r)$ emissions proxy (e.g. carbon), and $P(r)$ transfer and accessibility penalty. Weights $\alpha, \beta, \gamma, \delta$ are configurable. The service returns one or more Pareto-optimal or weighted-optimal routes.

## Optimization Criteria

- **Travel time**: Total journey time including in-vehicle time, walking, waiting, and transfers. Primary minimand for many use cases.
- **Cost**: Fare or generalised cost. May be per-mode or total; configurable for different fare models.
- **Carbon footprint**: Estimated CO2 or equivalent for the journey. Supports low-carbon routing when data (e.g. vehicle type, occupancy) is available.
- **Transfer penalties**: Penalise number of transfers or transfer time to favour simpler journeys when appropriate.
- **Accessibility-aware constraints**: Optional constraints or penalties for segments or modes that are not accessible (e.g. steps-only, no wheelchair access). Depends on availability of accessibility metadata in the twin.

Weights or constraints are configurable so that different applications can emphasise time, cost, or carbon; exact formulation will be documented in the API and in the implementation.

## Graph and Weights

The routing graph extends the digital twin with:

- Transit edges (bus, metro, minibus) with schedule or frequency-based travel times and fares.
- Walking and cycling edges with times derived from distance and current conditions where applicable.
- Transfer edges between modes with optional penalties.

Edge weights are updated from the digital twin (current speed, delays, incidents). Forecasts may be used for departure-time-dependent routing in future.

## Output

The service returns one or more Pareto-optimal or weighted-optimal routes with segment-by-segment breakdown (mode, time, cost, carbon if available). Response format is specified in [api-spec.md](api-spec.md).

## Limitations

- Routing quality depends on twin accuracy and coverage. Gaps or stale data will affect recommendations.
- Fare and carbon models are simplifications; they are not guaranteed accurate for all operators or vehicle types.
- Accessibility data may be incomplete; routing should not claim full accessibility compliance unless explicitly documented.

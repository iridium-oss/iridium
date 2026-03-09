# Optimization and Objectives

This document formalizes the optimization objectives used in IRIDIUM, in particular routing, so that code and documentation are consistent.

## Routing Objective

The route planner minimizes a **weighted sum** of time, cost, and carbon. The weight vector depends on the `optimize` parameter.

Let \( d \) = total duration (minutes), \( c \) = total cost, \( k \) = total carbon (kg). The objective value is:

- **time** (default): \( 1.0 \cdot d + 0.1 \cdot c + 0.5 \cdot k \)
- **cost**: \( 0.2 \cdot d + 2.0 \cdot c + 0.1 \cdot k \)
- **carbon**: \( 0.1 \cdot d + 0.2 \cdot c + 5.0 \cdot k \)

Implemented in `routing/plan.py` as `_weight(optimize, duration_min, cost, carbon_kg)`. All terms use non-negative coefficients. Units: duration in minutes, cost in application units, carbon in kg. Normalization is implicit in the chosen coefficients; no per-request normalization is applied. Configurable weights with validation can be added in a future revision.

## Forecast Loss (Experimental)

For a future learned forecasting model, the primary loss is MAE (see [modeling.md](modeling.md)). No production forecast training is currently in use.

## Constraints

- Routing: allowed modes filter edges; no explicit capacity or time-window constraints in the baseline. Path search is over the static graph (travel_time_min, cost, carbon_kg per edge).
- Transfer penalties: not implemented in the baseline; can be added as an additive term or edge cost.

## Multi-Objective Coherence

The routing objective is a single scalar combination of time, cost, and carbon. Multi-criteria ranking (e.g. Pareto alternatives) is planned; the current API returns one alternative per request. The implemented formula is consistent across all three modes and is documented here and in code comments.

## Sensitivity and Stability

Parameter behavior is fixed in code. Arbitrary or unbounded weights are not accepted from the client. If configurable weights are added, they will be validated to prevent unstable or degenerate objectives.

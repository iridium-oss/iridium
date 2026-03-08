# Routing Service

Multimodal route planning baseline. Computes routes from origin to destination using the digital twin graph, with configurable optimization (time, cost, carbon). Supports bus, metro, minibus, walking, cycling. This is an initial optimization baseline, not a full production journey planner.

## Implemented

- plan_routes(RouteRequest) returns RouteResponse with one or more alternatives.
- Origin/destination snapped to nearest graph nodes.
- Weighted scoring for time, cost, and carbon; mode filter and max_transfers respected in graph filter.
- Route segments include mode, duration, cost, carbon for transparency.

## Future

- Full schedule-based transit and transfer penalties.
- Real-time weights from digital twin and forecast.
- Accessibility constraints and multiple Pareto alternatives.

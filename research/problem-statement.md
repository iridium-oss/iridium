# Problem Statement

This document states the core problem that IRIDIUM addresses and the assumptions underlying the project. It is intended to align the team and contributors and to provide a basis for methodology and evaluation.

## Problem

Urban mobility systems in growing cities face several interconnected challenges:

1. **Congestion and unreliability**: Traffic congestion and unpredictable travel times reduce efficiency and quality of life. Effective prediction can support both operational decisions and user planning.

2. **Fragmented data**: Useful prediction and optimization require combining multiple data sources (sensors, telemetry, weather, events). These sources are often held by different entities, in different formats, and under different legal and contractual constraints. Centralising raw data is often infeasible or undesirable.

3. **Privacy and regulation**: Mobility data can be highly identifying. Data protection regulations and organisational policies may prohibit or restrict centralisation of personal or device-level data. A system that can learn from distributed data without centralising it is therefore of interest.

4. **Multimodal planning**: Travellers and operators need routes that account for multiple modes (public transport, walking, cycling, etc.) and for objectives beyond time (e.g. cost, carbon footprint). Such routing must adapt to current and predicted network state.

5. **Equity and accessibility**: Transport investment and service design should be informed by evidence on who is underserved. Identifying spatial accessibility gaps and measuring mobility equity at district or zone level can support prioritisation. The methodology must be transparent and its limitations acknowledged.

6. **Anomalies and disruptions**: Incidents, closures, and large events cause sudden changes in demand and capacity. Detection and dynamic response (e.g. rerouting) improve resilience but require real-time or near-real-time data and clear operational caveats.

## Scope

IRIDIUM focuses on:

- Azerbaijani cities as the initial geographic context, with the intention that the architecture and methods can be generalised.
- Federated learning as the primary privacy-preserving training paradigm, with encrypted or secure aggregation of model updates.
- A digital twin as the central representation of the transport network and its state, fed by heterogeneous data sources and consumed by forecasting, routing, equity, and anomaly modules.
- Clear documentation of assumptions, limitations, and bias risks so that the system is interpretable and improvable by researchers and stakeholders.

## Assumptions

- Data holders (e.g. transport operators, municipalities) are willing to participate in a federated setup and to share model updates under agreed protocols; raw data may remain local.
- Sufficient data quality and coverage exist (or can be simulated) to train and evaluate forecasting and routing models. Gaps in coverage will be documented and their impact on fairness and accuracy acknowledged.
- The digital twin and APIs can be deployed in environments that meet the security and availability requirements of the use case (pilot or production). Exact requirements are deployment-specific.
- Policy and equity use of the Mobility Equity Score will be interpretation by humans; the system provides indicators and visualisation, not automatic policy decisions.
- The project does not assume prior certification or legal compliance; deployers are responsible for their own compliance assessment.

## Success Criteria (High Level)

- A working federated learning pipeline that produces a global model from distributed participants without centralising raw data. Formally, aggregation of local updates $\theta_k^{(t)}$ into $\theta^{(t+1)} = \sum_k (n_k / \sum_j n_j) \theta_k^{(t)}$ (FedAvg-style) with documented privacy and convergence assumptions.
- A forecasting component that produces short-horizon congestion (or equivalent) predictions with documented metrics and baselines.
- A multimodal routing service that uses the digital twin and supports configurable objectives (time, cost, carbon).
- A Mobility Equity Score module with district-level indicators and documented limitations.
- Anomaly detection and dynamic rerouting with documented operational caveats.
- Documentation and repository structure suitable for academic and institutional review and for open source contribution.

Detailed success criteria and evaluation metrics are in [evaluation-plan.md](evaluation-plan.md). Risks and limitations are in [risks-and-limitations.md](risks-and-limitations.md).

# System Overview

This document provides a top-level overview of IRIDIUM for both technical and non-technical readers. Terminology is kept formal and consistent with the [glossary](glossary.md).

## What IRIDIUM Is

IRIDIUM is a real-time urban mobility prediction and optimization platform for Azerbaijani cities. It aims to support better traffic prediction, multimodal journey planning, equity-aware policy discussion, and response to incidents and events. The system is designed so that sensitive mobility data can remain under the control of data holders; model learning is performed in a federated way, with only encrypted or otherwise privacy-preserving updates shared.

## Core Concepts

- **Federated learning**: Model training is distributed. Each participant trains on local data and sends only model updates to an aggregation service. Raw data does not leave the participant.
- **Digital twin**: A dynamic, machine-readable representation of the city's transport network and its current state (e.g. speeds, occupancy, incidents). The twin is updated from multiple data sources and used for prediction and routing.
- **Four modules**: Forecasting (short-horizon congestion), Multimodal Routing (time, cost, carbon), Mobility Equity Score (accessibility gaps), and Anomaly Detection and Dynamic Rerouting (incidents, closures, events).

## Intended Users and Use Cases

- **Transport planners and operators**: View forecasts and equity metrics; plan interventions and prioritise infrastructure.
- **Travellers**: Get multimodal routes that account for current conditions and optional objectives (e.g. lowest carbon).
- **Researchers and civic innovators**: Use open documentation and, where applicable, open source components to reproduce or extend the work.

## High-Level Data Flow

The digital twin is a graph $G = (V, E)$ with time-varying state; forecasting produces $\hat{Y}_{t+1:t+H}$ from $X_{t-T+1:t}$ and $G$; routing minimises $J(r) = \alpha T(r) + \beta C(r) + \gamma E(r) + \delta P(r)$. See [symbol-glossary.md](symbol-glossary.md) for notation.

1. Data sources (sensors, telemetry, weather, events, etc.) feed into ingestion pipelines.
2. Ingestion validates and normalises data, then updates the digital twin.
3. The digital twin drives the forecasting engine and the routing service.
4. In the federated setting, local nodes train on local data and send updates to the aggregator; the aggregator produces a global model used for inference.
5. Anomaly detection consumes the same or related streams and updates the twin and routing with incident or closure information.
6. APIs expose predictions and routes to the frontend and external systems.

## What IRIDIUM Does Not Claim

- IRIDIUM does not claim to be legally compliant in any specific jurisdiction. Deployers must conduct their own compliance and risk assessment.
- The project does not claim production deployment, formal certifications, or partnerships unless explicitly stated in official communication.
- Current documentation describes proposed or planned behaviour; implementation status is stated in the repository and in the roadmap.

## Where to Go Next

- **Architecture and components**: [architecture.md](architecture.md), [federated-learning.md](federated-learning.md), [digital-twin.md](digital-twin.md).
- **Data and models**: [data-sources.md](data-sources.md), [modeling.md](modeling.md), [routing.md](routing.md), [fairness.md](fairness.md), [anomaly-detection.md](anomaly-detection.md).
- **Operations**: [deployment.md](deployment.md), [api-spec.md](api-spec.md).
- **Terms**: [glossary.md](glossary.md).

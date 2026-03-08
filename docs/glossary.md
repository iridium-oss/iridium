# Glossary

Definitions of key terms used in the IRIDIUM documentation and codebase. Use consistent terminology in contributions.

**Aggregation (federated)**: The process of combining model updates from multiple participants into a single global model. The aggregation service does not receive raw data.

**Digital twin**: A dynamic, machine-readable representation of the urban transport system: graph topology plus time-varying state (speeds, occupancy, incidents) and metadata. Updated from ingestion and used by forecasting and routing.

**Federated learning**: A training paradigm in which data remains at participant sites; only model updates (e.g. gradients or encrypted weights) are sent to an aggregator. Used in IRIDIUM to support privacy-preserving and regulation-aware deployment.

**Forecasting engine**: The component that produces short-horizon (e.g. 2 to 3 hour) predictions of congestion or traffic state using spatio-temporal models and the digital twin.

**Ingestion**: The pipeline that receives data from external sources (sensors, telemetry, weather, events), validates and normalises it, and updates the digital twin.

**Local training node**: A participant-side component that trains the model on local data and sends only model updates to the aggregation service.

**Mobility Equity Score**: A set of district-level indicators intended to identify spatial accessibility gaps and support data-driven infrastructure prioritisation. Documented in [fairness.md](fairness.md).

**Multimodal routing**: Route computation across multiple modes (bus, metro, minibus, walking, cycling) with configurable objectives (time, cost, carbon) and transfer penalties.

**Participant**: An entity that holds data and runs a local training node in the federated setup (e.g. transport operator, municipal node).

**ST-GNN**: Spatio-temporal graph neural network. A class of models that operate on a graph structure and capture temporal dynamics; used for congestion forecasting in IRIDIUM.

**Twin**: Short for digital twin.

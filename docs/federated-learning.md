# Federated Learning in IRIDIUM

This document explains how federated learning is used in IRIDIUM, the flow of model updates, and the benefits and limitations. The architecture is designed to support privacy-preserving and regulation-aware deployment; it does not by itself guarantee legal compliance.

## Implementation Status

Federated learning orchestration is not yet implemented. The repository documents the architecture, data flow, and privacy rationale; the current baseline uses a single in-memory digital twin and heuristic or rule-based modules. This section and the following describe the intended design for future implementation.

## Privacy by Design

Raw personal data (e.g. individual trip records, device identifiers) is not centralised. Each participant keeps data on their own infrastructure. Only model-related artefacts (e.g. gradients, encrypted weights) are sent to the aggregation service. This reduces the risk of bulk data leakage and supports deployment in environments where data cannot leave a jurisdiction or organisation.

## Federated Objective and Aggregation

The global objective is to minimise a weighted sum of local losses: $\min_{\theta} \sum_{k=1}^{K} p_k \, \mathcal{L}_k(\theta)$ where $K$ is the number of clients, $p_k$ the weight of client $k$ (e.g. $n_k / \sum_j n_j$ with $n_k$ local sample count), and $\mathcal{L}_k$ the local loss. After each round, FedAvg-style aggregation updates the global parameters:

$$
\theta^{(t+1)} = \sum_{k=1}^{K} \frac{n_k}{\sum_j n_j} \theta_k^{(t)}
$$

where $\theta_k^{(t)}$ is the local model at client $k$ after round $t$.

## Local Model Training

Each participant runs a local training process. The process:

- Reads only data that the participant is authorised to use.
- Computes model updates (e.g. gradients or weight deltas) using the current global model and local data.
- Optionally applies local privacy mechanisms (e.g. clipping, noise) before sending updates.
- Sends the updates to the aggregation service over a secure channel.

The global model may be a full model or a component (e.g. an encoder). The exact architecture will be documented in the modeling and deployment docs as the implementation evolves.

## Encrypted Model Updates

The protocol is designed to support encrypted or secure aggregation. Options include:

- **Secure aggregation**: Updates are encrypted so that the aggregator can compute the sum (or another combination) without reading individual updates.
- **Differential privacy**: Noise is added to updates or to the aggregate to bound the information leaked about any single participant's data.

The reference implementation will document which mechanism is used and under what assumptions. Encryption and key management are deployment responsibilities.

## Aggregation Flow

1. The aggregation service announces the current global model (or checkpoint) and training configuration.
2. Participants pull the model, train locally, and push updates (possibly encrypted).
3. The aggregator combines updates (e.g. weighted average by sample count or by trust weight) and produces a new global model.
4. The new model is distributed to participants for the next round or for inference.

Participation may be synchronous (all participants contribute in each round) or asynchronous (updates are applied as they arrive). The chosen strategy affects convergence and will be documented with the implementation.

## Benefits

- **Data locality**: Raw data stays at the participant; only model updates leave the site.
- **Regulation-aware**: The design can support deployment where data residency or sector-specific rules restrict centralisation.
- **Scalability**: New participants can join by running a local node and agreeing to the protocol; the central aggregator does not need to store raw datasets.

## Limitations

- **Non-IID data**: If participant data distributions differ strongly, the global model may underperform for some participants. Mitigations (e.g. personalisation, weighted aggregation) are an area of ongoing work.
- **Communication and compute**: Federated training requires multiple rounds of communication and local compute; latency and resource use are non-trivial.
- **Byzantine and free-riding**: Malicious or faulty participants can skew the aggregate. Robust aggregation and optional verification mechanisms are considered but not guaranteed in the initial release.
- **No legal guarantee**: The architecture is designed to support privacy and regulatory alignment; deployers must obtain their own legal and compliance advice.

## Assumptions and Open Questions

- Participants are identified and authenticated; the trust model (e.g. all participants trusted, or Byzantine-resistant aggregation) will be documented.
- Network connectivity and availability assumptions for aggregation rounds are to be specified per deployment.
- Formal privacy guarantees (e.g. differential privacy parameters) will be stated where applicable; default settings may not meet all regulatory requirements.

Open questions include: choice of secure aggregation library, handling of stragglers, and personalisation strategies. These will be updated in the repository as decisions are made.

# Federated Learning Privacy

What secure aggregation and differential privacy do in IRIDIUM FL, and what they do not guarantee.

## Plain Federated Learning (Default)

- Clients send model updates (parameters) to the server. The server can see each client's updates and aggregates them (e.g. FedAvg).
- Raw training data does not leave the client. That reduces exposure of raw data but does not by itself provide formal privacy guarantees against inference on the updates.

## Secure Aggregation

- **Purpose**: The server learns only the aggregate of client updates, not individual updates. Implemented via Flower's secure aggregation workflow when enabled.
- **Status**: Not enabled by default. When enabled, document it in run config and API privacy-status.
- **What it protects**: Confidentiality of individual updates during aggregation. It does not protect against a malicious server or client outside the protocol; it does not provide differential privacy.

## Differential Privacy (DP)

- **Purpose**: Bounds the information leaked about any single training example (e.g. via clipping and noise).
- **Status**: Optional; not enabled by default. When implemented, use clipping and noise configuration and record privacy-related settings in metadata.
- **What it does not do**: DP does not automatically make the system compliant with GDPR or other regulations. Privacy accounting and production suitability depend on the exact deployment, threat model, and parameters. Do not market DP as magic or automatic compliance.

## Capability Matrix

| Mode | Plain FL | Secure aggregation | DP | Notes |
|------|----------|--------------------|-----|------|
| Default | Yes | No | No | FedAvg only. |
| With SecAgg | Yes | Yes | No | When enabled. |
| With DP | Yes | No | Yes | When enabled; document parameters. |
| SecAgg + DP | Yes | Yes | Yes | When both enabled. |

## Warnings

- If DP is enabled without adequate configuration (e.g. missing noise or clipping), log a warning and record it in metadata.
- Do not overclaim privacy guarantees. Deployers are responsible for their own compliance and risk assessment.

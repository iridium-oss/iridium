# Data Contracts

This directory holds schema definitions and API contracts for IRIDIUM. Contracts define the shape of data exchanged between components and with external systems. They are the single source of truth for validation and for generated types or client code.

## Purpose

- **Ingestion**: Schemas for incoming data from sensors, telemetry, weather, events, and other sources. See `docs/data-sources.md` for context.
- **Digital twin**: Internal representation of the graph and time-varying state (nodes, edges, attributes). Used by ingestion, forecasting, and routing.
- **APIs**: Request and response schemas for the public API (forecast, routing, equity, anomalies). See `docs/api-spec.md` for endpoint overview.
- **Federated learning**: Message or payload schemas for model updates and global model distribution, where applicable.

## Format

Schemas may be defined in one or more of:

- **JSON Schema**: For REST APIs and JSON payloads. Tooling can generate validators and client types.
- **OpenAPI**: When the API is fully specified, OpenAPI (Swagger) can document endpoints and schemas together.
- **Other**: Protobuf, Avro, or IDL if the project adopts them for performance or compatibility.

Format and naming conventions will be documented here once adopted. Versioning (e.g. v1, v2 in filenames or schema IDs) will be used for backward-incompatible changes.

## Usage

- Backend and ingestion validate incoming data against these contracts.
- Frontend and external clients use contracts for request construction and response parsing.
- Documentation (e.g. `docs/api-spec.md`) references the contract files for authoritative field definitions.

## Contributing

Changes to contracts are breaking when they remove or rename fields or change types. Such changes require a new version and coordination with backend, frontend, and docs. See CONTRIBUTING.md and the pull request template; document impact on API and data flow.

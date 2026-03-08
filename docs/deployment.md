# Deployment

This document describes the baseline deployment options and a placeholder for future cloud or hybrid deployment. The implemented system can run locally or in Docker; persistence is optional.

## Implemented Options

- **Local development**: Run the API (uvicorn) and frontend (Vite dev server) from the repo; see [local-development.md](local-development.md). No database required for the baseline; the digital twin is in-memory.
- **Docker Compose**: `docker compose up -d` runs API, web (nginx serving Vite build), PostgreSQL, and Redis. The API container uses in-memory state; the database is initialised from `infrastructure/db/schema.sql` for future use. Web container proxies `/api`, `/health`, and `/version` to the API service.

## Target Environments

- **Development**: Local or containerised setup for contributors. Minimal external dependencies; synthetic or small real datasets.
- **Staging**: Cloud or on-premises environment that mirrors production for integration and performance testing. May use subset of data or anonymised data.
- **Production**: Full deployment for pilot or live use. May be hybrid: local training nodes at participants, aggregation and APIs in a central or distributed cloud.

## Components

- **Ingestion**: Services that consume data sources and write into the digital twin. May run per source or as a unified pipeline. Scaling is horizontal where the workload is partitionable.
- **Digital twin store**: Graph and time-series state. Candidate technologies: time-series DB, graph DB, or hybrid (e.g. PostgreSQL with extensions, or dedicated graph and TS stores). Choice depends on scale and query patterns.
- **Aggregation service**: Receives model updates from participants, runs aggregation, distributes the global model. Must be secure and auditable; may run in a trusted cloud or on-premises.
- **Inference and routing**: Stateless or lightly stateful services behind a load balancer. Scale out for availability and throughput.
- **Frontend**: Static or server-rendered web app; served via CDN or application server. Auth and API base URL are configuration.
- **Observability**: Logging (e.g. aggregated to a central log store), metrics (e.g. Prometheus or cloud metrics), and optional tracing. Dashboards and alerts are deployment-specific.

## Security and Privacy

- All participant-to-aggregator and client-to-API communication over TLS.
- Secrets (API keys, DB credentials, aggregation keys) from a secret manager; never in code or in plain config in the repo.
- Network segmentation so that ingestion, twin, and APIs can be isolated as needed.
- No raw personal data in central stores; see [federated-learning.md](federated-learning.md) and SECURITY.md.

## Configuration

- Environment-specific config (per env) for feature flags, endpoints, and limits.
- Schema and contract versions aligned across components; see `data-contracts/`.

## Future Additions

As the project matures, this document will be extended with: exact technology choices, scaling guidelines, backup and disaster recovery, and runbooks for common operations. Deployment status (e.g. pilot in city X) will be stated only when officially announced.

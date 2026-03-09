## Security architecture

This document describes the practical security posture of IRIDIUM as implemented in this repository. It focuses on supply chain controls, secret handling, API hardening, and data handling safeguards. It does not claim certifications or deployment level controls that are not present in the repository.

### Trust boundaries

- **Client**: Browser or API client calling the FastAPI service.
- **API service**: `apps/api` FastAPI application.
- **Provider connectors**: Service modules under `services/` that fetch or transform external data.
- **Data stores**: PostgreSQL (optional), Redis (optional), local recorded snapshots (optional), local caches (optional).
- **CI**: GitHub Actions workflows that lint, test, and run security checks.

### Data handling principles

- **No fabrication**: When a provider is missing, unavailable, or not configured, the API returns explicit `data_status` and provenance metadata instead of invented values.
- **Provenance first**: Provider outputs should carry source identifiers, timestamps, and source status. See `docs/data-provenance.md`.
- **Minimise raw payload exposure**: Provider connectors should avoid returning raw upstream payloads to API responses. Prefer normalized models with explicit fields and provenance.

### Secret handling

- **No secrets in git**: `.env` and secret files are ignored. CI runs secret scanning.
- **Local development**: Secrets live in `.env` only. See `docs/secrets-management.md` and `docs/environment.md`.
- **Logging**: Structured logs include redaction for common secret key names. Query strings are not logged by default.

### API hardening controls (repo level)

- **CORS discipline**: CORS origins are explicit. Methods and headers are restricted by default and configurable via settings.
- **Security headers**: Default headers prevent common browser side misuse for API responses. HSTS is disabled by default and must only be enabled behind TLS termination.
- **Request size limits**: Requests with large `Content-Length` are rejected to reduce accidental memory pressure and abuse surface.
- **Validation error hygiene**: Request validation errors do not echo the rejected input payload in API responses.

### Supply chain and CI controls

- **Pinned actions**: Workflows pin critical GitHub Actions to commit SHAs.
- **Secret scanning**: Gitleaks runs in CI on push and pull request.
- **Dependency scanning**: Python uses pip-audit, Node uses npm audit.
- **SAST and config scanning**: Bandit and Trivy config scanning run in CI and upload SARIF for review.
- **SBOM**: CI generates a CycloneDX JSON SBOM artifact.

### Repository policy assumptions

This repository includes CI workflows and a pull request template. Enforced branch protection is an organisational setting and is not controlled by code in this repository. Recommended baseline:

- Require pull requests for the default branch.
- Require CI workflows (lint, tests, security) to pass before merge.
- Require review for changes that add dependencies, modify workflows, or add new provider integrations.

### Deployment assumptions

This repository cannot enforce deployment settings such as TLS termination, network policies, or runtime secret managers. Production deployments should:

- Terminate TLS before the API, and only enable HSTS when TLS is guaranteed.
- Run API behind a reverse proxy with request rate limiting and additional request body limits.
- Use a secrets manager for production credentials.


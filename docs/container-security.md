## Container security

This repository ships Dockerfiles for the API and web services and uses Docker Compose for local development. The baseline hardening goals are least privilege, minimal attack surface, and predictable builds.

### Image hardening controls

- **Non root**: Web runs on an unprivileged nginx image. API runs as a non root user.
- **Minimal images**: API uses Python slim base. Web uses multi stage build and a runtime nginx image.
- **Health checks**: API image includes a healthcheck; compose also defines healthchecks.
- **No secrets baked in**: Images are built without embedded credentials. Secrets are passed via environment at runtime.

### CI scanning

CI runs Trivy config scanning against the repository configuration and uploads SARIF for review. This includes Dockerfiles and Compose files.

### Local development guidance

- Do not expose local stacks to untrusted networks.
- Use `.env` for local overrides and keep it out of git.
- For Postgres and Redis used in demos, treat credentials as local only and replace for any non local deployment.


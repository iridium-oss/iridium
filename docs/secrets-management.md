# Secrets Management

Sensitive configuration (API keys, database passwords, telemetry credentials) must not be committed to the repository.

## Rules

- **Do not commit**: `.env`, any file containing API keys or passwords, or raw personal or device-level traces.
- **Use `.env` for local development**: Copy `.env.example` to `.env`, set secrets locally, and add `.env` to `.gitignore` (already standard). Never commit `.env`.
- **CI**: Use repository secrets or environment secrets in GitHub Actions (or equivalent) for any key needed in CI. Do not paste secrets into workflow files.
- **Production**: Use a secrets manager (e.g. vault, cloud provider secrets) or environment injection; do not bake secrets into images or config files in version control.

## Sensitive variables

| Variable | Sensitivity | Notes |
|----------|-------------|--------|
| POSTGRES_PASSWORD | High | Database access. |
| TRAFFIC_API_KEY | High | Provider billing and access. |
| TRACCAR_USER, TRACCAR_PASSWORD | High | Telemetry server access. |
| POSTGRES_DSN | High if contains password | Prefer separate POSTGRES_* vars. |

Other variables in `.env.example` are non-sensitive or optional. When adding new providers, document sensitive variables in this file and in docs/environment.md.

## Rotation

Rotate credentials periodically and when compromise is suspected. Update `.env` (local) or the secrets store (production); no need to change code unless the variable name or provider contract changes.

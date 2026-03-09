## Dependency security

IRIDIUM uses Python (backend and services) and Node (web). This document defines the minimum dependency hygiene rules enforced in CI and expected during development.

### Rules

- **No unreviewed dependency additions**: New dependencies must be justified in the pull request summary and reviewed for license and security impact.
- **Lockfile discipline**: Node uses `package-lock.json` and CI uses `npm ci`. Do not edit lockfiles manually.
- **Pin sensibly**: Runtime dependencies may use compatible ranges, but CI and container builds must be reproducible. Prefer explicit versions for toolchain dependencies and avoid floating tags for base images.

### CI checks

- **Python vulnerabilities**: `pip-audit` runs in CI against the installed environment and fails the workflow on findings.
- **Node vulnerabilities**: `npm audit --audit-level=high` runs in CI for `apps/web`.
- **SBOM**: CI emits a CycloneDX JSON SBOM artifact for review and downstream scanning.

### Safe upgrade workflow

1. Update dependencies in a focused pull request.
2. Run unit and integration tests.
3. Review vulnerability outputs from CI.
4. For security relevant upgrades, include a short impact note:
   - what changed
   - why it is safe for IRIDIUM
   - whether configuration changes are required

### Handling vulnerability findings

- Prefer upgrading to a fixed version.
- If no fix exists, mitigate by:
  - reducing exposure (disable feature or provider by default)
  - adding timeouts and input validation at boundaries
  - documenting risk in the pull request and tracking a follow up issue


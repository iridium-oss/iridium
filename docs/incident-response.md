## Incident response

This document describes a practical response workflow for security and data handling incidents related to IRIDIUM deployments and the repository.

### Reporting security issues

- Do not open a public issue for suspected vulnerabilities.
- Use GitHub Security Advisories for private disclosure when available.

### Initial triage

1. Identify the affected component (API, provider connector, container build, CI).
2. Determine whether secrets may be exposed:
   - committed secret in git
   - leaked secret in logs
   - leaked secret in API response
3. Determine data impact:
   - any raw telemetry or personal traces involved
   - any licensed partner payloads exposed

### Containment

- Revoke and rotate credentials that may be exposed.
- Disable affected provider integrations by configuration where possible.
- Reduce exposure surface by limiting access and halting ingestion jobs if required.

### Remediation

- Patch code, add regression tests for the failure mode, and document the change.
- For CI or dependency issues, update workflows and lockfiles as needed.
- For container issues, rebuild and redeploy images.

### Post incident actions

- Write a short internal summary: timeline, root cause, impact, and mitigation.
- Add follow up items to prevent recurrence (for example additional redaction keys, stricter validation, improved timeouts).

### Related operational guidance

For non security runtime incidents (provider downtime, missing configuration) see `docs/incident-playbook.md`.


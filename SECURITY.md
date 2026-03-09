# Security Policy

## Supported Versions

Security fixes are handled on a best-effort basis. Pre-1.0 releases may change rapidly, and security patches are typically applied to the default branch first. When releases exist, security relevant fixes should be reflected in release notes.

## Reporting a Vulnerability

We take security seriously. If you believe you have found a vulnerability in IRIDIUM, please report it through responsible disclosure.

**Process:**

1. Do not open a public issue for the vulnerability.
2. Contact the maintainers privately. Use the contact method indicated in the repository (e.g. GitHub Security Advisories, or a designated email if listed). If no method is listed, open a private security advisory via the repository's Security tab.
3. Provide a clear description of the issue, steps to reproduce (if applicable), and the impact you believe it has. Include the version or commit range affected.
4. Allow a reasonable time for the maintainers to acknowledge and respond (typically within 14 days).
5. Do not disclose the vulnerability publicly until the maintainers have had a chance to address it or have agreed on a disclosure timeline.

We will acknowledge receipt, work with you to understand and validate the issue, and keep you informed of the intended remediation and disclosure plan where appropriate.

## Scope

In scope for security reporting:

- Authentication, authorization, or session handling flaws (when present).
- Injection, deserialization, or other code execution vulnerabilities.
- Exposure of sensitive data (credentials, personal data, or internal configuration) through the application or its dependencies.
- Weaknesses in cryptographic usage or key management in the codebase (when present).

Out of scope:

- Issues in third-party services or dependencies that are not under our control (report to the respective vendor; we still welcome being informed).
- Best-effort or theoretical issues without a concrete exploit path.
- General hardening or policy recommendations that are not tied to a specific vulnerability.

## Privacy-Sensitive Data

IRIDIUM is a mobility platform and deployments may process sensitive telemetry depending on enabled integrations (for example consent based device traces, partner feeds, operator feeds). This repository should not contain raw personal data or committed secrets. Despite that:

- Deployers are responsible for their own data handling and compliance with applicable law.
- Security discussions and patches must avoid exposing sensitive operational details (e.g. real deployment topology, real credentials, or real user data). When sharing proof-of-concept or logs, redact or anonymize appropriately.

## Disclosure

We will work with reporters in good faith. We do not support legal action against researchers who report vulnerabilities in good faith and follow this process. Public disclosure will be coordinated with the reporter where possible, and credit will be given unless the reporter prefers to remain anonymous.

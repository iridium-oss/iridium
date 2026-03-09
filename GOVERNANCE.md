# Governance

This document describes the governance model for the IRIDIUM project. The model is lightweight but structured to ensure clear ownership, transparent decision-making, and a path for long-term sustainability.

## Maintainers

The following individuals are founding maintainers of the IRIDIUM repository. They are responsible for day-to-day stewardship, code and documentation review, and release decisions within the scope of this document.

**AI Engineering**

- Olaf Yunus Laitinen Imanov
- Malahat Ismayilova
- Fidan Bagirova

**Fullstack & Frontend**

- Amina Sadiqzade (Frontend)
- Aslan Ibadullayev (Fullstack)

Maintainers are expected to act in the best interest of the project, follow the Code of Conduct, and uphold the contribution and security policies. New maintainers may be added by consensus of existing maintainers, with criteria and process documented in this file or in a separate document as the project grows.

## Decision Making

- **Routine changes**: Bug fixes, documentation updates, dependency updates, and small feature work follow the normal pull request process. Any maintainer may review and merge once the PR template and CI requirements are satisfied.
- **Significant changes**: Features that affect public APIs, architecture, or data contracts require review from at least one maintainer from a relevant area (e.g. backend, models, frontend) and consensus among maintainers when in doubt.
- **Disputes**: If maintainers disagree on a decision, the default is to discuss in the open (e.g. in an issue or PR). If consensus cannot be reached, the matter may be deferred or resolved by a simple majority of maintainers, with a short rationale recorded.

## Review Process

- All code and substantive documentation changes enter the repository via pull requests.
- At least one maintainer must approve before merge. For areas touching privacy, security, or federated learning, an additional review from a maintainer familiar with that area is encouraged.
- CI (lint, tests, docs checks) must pass. Maintainers may request additional tests or documentation before approval.
- The pull request template (summary, motivation, technical changes, testing, documentation, privacy/security) must be completed. Incomplete or placeholder answers may delay review.

## Release Stewardship

- Releases are cut by maintainers. Versioning follows semantic versioning (SemVer) where applicable: major.minor.patch for stable APIs.
- Release notes are derived from CHANGELOG.md. The Unreleased section is moved into a versioned section at release time.
- Pre-release and development versions may use a suffix (e.g. 0.1.0-dev). The supported versions and support policy are documented in SECURITY.md.

## Architectural Change Proposals

For changes that affect system architecture, data contracts, or long-term technical direction:

- Propose the change in a dedicated issue or document (e.g. in `docs/` or `research/`) with a clear problem statement, options, and recommendation.
- Allow time for maintainers and the community to comment (e.g. one to two weeks for non-urgent items).
- Decision is made by maintainer consensus. The outcome and rationale are recorded (e.g. in the issue or in ROADMAP.md / architecture docs).

## Core Contributors

Contributors who provide sustained, high-quality contributions may be recognized as core contributors. Recognition is at the discretion of maintainers and may be reflected in the README or CONTRIBUTING.md. Core contributors do not automatically receive merge rights; maintainer status is separate and follows the process above.

## Amendments to Governance

Changes to this governance document are made via pull request. They require approval from a majority of maintainers. Substantial changes (e.g. change in maintainer roles or decision-making process) should be announced in an issue or release note so that contributors and users are aware.

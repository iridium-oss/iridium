# Contributing to IRIDIUM

Thank you for your interest in contributing to IRIDIUM. This document describes the project philosophy, conventions, and expectations for contributors. For a high-level overview of the product and what is implemented, see [docs/product-scope.md](docs/product-scope.md) and [docs/reviewer-guide.md](docs/reviewer-guide.md).

## Project Philosophy

IRIDIUM is an open source urban mobility platform with a research-oriented and institutional tone. Contributions should align with:

- Privacy by design: no centralization of raw personal data; federated and privacy-preserving patterns where applicable.
- Documentation and code evolving together; every change that affects behaviour or APIs should be reflected in docs where relevant.
- Formal, professional language in all user-facing and repository-facing text. No casual or marketing language.
- Clarity over cleverness; maintainability and reproducibility are priorities.

## Branch Naming

- Use short, descriptive branch names in lowercase, with words separated by hyphens.
- Prefix with category when helpful: `feature/`, `fix/`, `docs/`, `refactor/`, `chore/`.
- Examples: `feature/routing-api`, `fix/ingestion-timeout`, `docs/architecture-update`.

## Commit Messages

- Use the imperative mood ("Add handler" not "Added handler").
- First line: concise summary (about 50 characters or fewer when practical). No period at the end.
- Optional body: explain what and why, not how, when the change is non-trivial. Wrap at 72 characters.
- Reference issues or PRs where relevant (e.g. "Fixes #123").

Example:

```
Add validation for sensor payload timestamps

Reject records older than configured max age to avoid polluting
the digital twin with stale data. Config key: ingestion.max_age_seconds.
```

## Pull Request Expectations

- One logical change per PR when possible. Large changes should be split into reviewable pieces.
- Fill out the pull request template completely: summary, motivation, technical changes, testing, documentation impact, and privacy/security considerations.
- Ensure CI passes. Fix lint and test failures before requesting review.
- All user-facing or repository-facing text (comments, docs, commit messages) must remain formal and professional.
- Do not use emojis. Do not use em dash or en dash; use a normal hyphen only when needed.

## Issue Reporting

- Use the appropriate template: bug report, feature request, or research task.
- Provide enough context for maintainers to reproduce or evaluate (environment, steps, expected vs actual behaviour).
- For bugs: version or commit, logs or error messages (redact sensitive data).
- For feature or research issues: clear problem statement and proposed direction.

## Documentation Standards

- Docs live in `docs/`. Research-oriented material lives in `research/`.
- Use clear headings, short paragraphs, and lists where they improve readability.
- Define acronyms on first use; use the [glossary](docs/glossary.md) for key terms.
- Do not claim deployment status, benchmarks, or compliance that are not yet true; use "planned", "proposed", or "designed to support" as appropriate.

## Coding Standards

- Follow the style enforced by the project (e.g. formatters and linters in CI). See `.editorconfig` and workflow files.
- Prefer explicit over implicit; avoid magic numbers and undocumented assumptions.
- Add or update tests for behaviour changes. Keep tests deterministic and fast where possible.
- Handle errors explicitly; log meaningfully without exposing sensitive data.

## Review Etiquette

- Reviews should be constructive and focused on correctness, clarity, and alignment with project standards.
- Approvers should verify that documentation and privacy/security considerations have been addressed.
- All discussion should remain professional and on-topic.

## Language and Tone

All user-facing and repository-facing language (README, docs, comments, commit messages, issue/PR content) must remain formal and professional. Avoid hype, vague claims, and casual phrasing. This requirement applies to every contribution.

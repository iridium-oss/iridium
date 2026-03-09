# CI and CD

This repository uses GitHub Actions for continuous integration. It does not claim production deployment automation.

## Workflows

Files under `.github/workflows/`:

- `lint.yml`: Ruff, Black, and mypy for Python.
- `ci.yml`: Python tests and frontend tests.
- `docs.yml`: Docs structure checks and basic link checks.

## Expectations

- Pull requests should pass lint and tests before merge.
- CI is intended to be reproducible. Dependencies are installed from project metadata, and caches are used for speed.
- Coverage upload is best-effort and must not block merges. Coverage thresholds are enforced in the repository configuration.

## Local equivalence

Commands correspond to:

- `make lint`
- `make test`
- `make typecheck`


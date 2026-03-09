# Tests

This directory contains the test suite for IRIDIUM: unit tests, integration tests, and contract tests that validate behaviour and compatibility across components.

## Purpose

- **Unit tests**: Test individual functions, classes, or modules in isolation. Mock external dependencies (APIs, databases) where appropriate.
- **Integration tests**: Test interaction between components (e.g. ingestion to twin, API to routing). May use in-memory or test databases and synthetic data.
- **Contract tests**: Validate that request and response payloads conform to the shared schemas in `packages/schemas`. Ensure backward compatibility when schemas change.
- **CI**: The test suite is run in CI (`.github/workflows/ci.yml`). All tests must pass before merge unless explicitly excluded with justification.

## Structure

Structure may mirror the source layout (e.g. `tests/backend/`, `tests/models/`, `tests/data_contracts/`) or be organised by type (e.g. `tests/unit/`, `tests/integration/`). Conventions will be documented here as they are adopted. Shared fixtures and test data (synthetic only) may live under `tests/fixtures/` or similar.

## Running Tests

- From the repository root: `pytest tests/` (or the equivalent for the project's test runner). See root README or CONTRIBUTING for the exact command and environment setup.
- Tests must be deterministic. Avoid reliance on system time, random seeds, or external services unless explicitly mocked or stubbed.
- No real personal data or production credentials in tests or fixtures.

## Contributing

New behaviour should be covered by tests where practical. Bug fixes should include a regression test. See CONTRIBUTING.md for review expectations and the pull request template for the testing section.

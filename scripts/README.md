# Scripts

This directory holds operational and development scripts for IRIDIUM: one-off tasks, local setup, data preparation, and deployment helpers. Scripts are not part of the core application runtime but support development, testing, and operations.

## Purpose

- **Setup**: Scripts to create virtual environments, install dependencies, or initialise local databases or twin stores.
- **Data preparation**: Generation of synthetic data, or transformation of sample data for development and tests. No production or sensitive data in the repository.
- **Migration**: Schema or data migrations for the digital twin or backend stores when applicable.
- **Deployment**: Helper scripts for building, tagging, or deploying (e.g. Docker build, asset upload). Deployment-specific secrets and credentials must not be committed.
- **Maintenance**: Cleanup, backup, or reporting scripts used by maintainers or in CI.

## Conventions

- Scripts should be documented at the top (purpose, usage, required env or args). Use the project's formal tone; no emojis.
- Prefer idempotency where possible so that re-running a script does not cause unintended side effects.
- Dependencies (e.g. Python packages) should be listed in the project's dependency files or in a comment at the top of the script. Avoid ad-hoc installs that are not tracked.

## Safety

- Scripts must not hardcode secrets, credentials, or paths to sensitive data. Use environment variables or config files that are excluded from version control.
- Destructive operations (e.g. drop table, delete all) should require an explicit flag or confirmation when run interactively.

## Contributing

New scripts should be added with a short note in this README or in the root CONTRIBUTING if they affect the contribution workflow. See the pull request template for documentation impact.

# Source (Shared Libraries and Utilities)

This directory holds shared source code used across the IRIDIUM project: libraries, utilities, and common types that are consumed by the backend, models, or other components.

## Purpose

- **Avoid duplication**: Common logic (e.g. config loading, logging, schema validation) lives here so that backend and models do not reimplement it.
- **Consistent contracts**: Shared types and helpers that align with `data-contracts/` and with the digital twin representation.
- **Testing**: Shared code is unit-tested here or via dependents; the repository test suite may reference this package.

## Structure

Structure will be established as the project grows. Expected subdirectories may include:

- `iridium/common`: Config, logging, and environment utilities.
- `iridium/schemas`: Validation or binding to data contracts (when implemented).
- `iridium/graph`: Shared graph or digital-twin abstractions if used by both backend and models.

Exact layout and package names will follow the language and framework chosen for the backend and models (e.g. Python packages under `src/`).

## Usage

Other components (backend, models) depend on this package via the project's dependency management (e.g. pip install in editable mode, or workspace package). See the root README and CONTRIBUTING for build and test instructions.

## Contributing

Changes to shared code must preserve backward compatibility or follow a versioned API. See CONTRIBUTING.md and the pull request template for documentation and testing expectations.

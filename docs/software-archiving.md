# Software Archiving and Long-Term Availability

IRIDIUM is maintained as an open source project. This document describes how the project supports long-term preservation and citation.

## Primary Host

- **Code and issues**: https://github.com/iridium-oss/iridium
- **License**: EUPL-1.2 (see LICENSE in the repository).

## Archiving Strategy

| Mechanism | Purpose |
|-----------|---------|
| GitHub releases | Versioned snapshots; trigger Zenodo archival when Zenodo is linked. |
| Zenodo | Assigns a persistent DOI per release for formal citation. |
| CITATION.cff | Enables tools and platforms to suggest citation text; used by Zenodo and others. |

## Versioning

- Version is set in pyproject.toml and CITATION.cff. When cutting a release, update both and add an entry to CHANGELOG.md.
- Semantic versioning (major.minor.patch) is used. Pre-release versions (e.g. 0.2.0-dev) are not assigned a Zenodo DOI unless explicitly released as a release tag.

## What Is Archived

- Source code, documentation under docs/, and configuration files. Data (e.g. OSM extracts, recorded snapshots) are not stored in the repository; provenance and fetch instructions are documented so that data can be re-obtained where legally and technically possible.

## Reproducibility

- Documentation describes how to run the stack (local development, Docker, environment variables). Research artifacts and evaluation plans are in the research/ directory. Reproducibility of results depends on using a specific release version and the documented data and environment setup.

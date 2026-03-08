# Badge Policy and Inventory

This document defines which badges appear in the README, how they are validated, and when scholarly badges may be activated.

## Policy

- **Allowed**: Badges that reflect a real repository artifact, workflow, or external resource. Each must resolve (image URL and click target return HTTP 2xx or 3xx).
- **Forbidden**: Fabricated DOIs, arXiv identifiers, coverage percentages not produced by the repo, or badges that point to non-existent workflows or releases.
- **Scholarly activation**: Zenodo DOI and arXiv badges may be added to the visible README badge bar only after a real identifier is assigned. Until then, they are prepared in this document and in release/preprint checklists.

## Badge Groups

| Group | Purpose | Examples |
|-------|---------|----------|
| Repository health | License, release, activity | License, last release, issues, PRs, stars |
| Workflow and quality | CI, lint, docs | CI status, Lint status, Docs status |
| Package and runtime | Stack and integrations | Python, Node, Docker, PostGIS (static if no dynamic badge) |
| Documentation and scholarly | Docs and citation | Docs status; DOI/arXiv only when real ID exists |
| Operational | Live endpoints | Only if backed by real health or status endpoint |

## Inventory

| Badge | Source | Live | Link target | Validation |
|-------|--------|------|--------------|------------|
| License | Shields.io / GitHub | Yes | LICENSE in repo | scripts/verify_badges.py |
| CI | GitHub Actions | Yes | .github/workflows/ci.yml | Workflow name: CI |
| Lint | GitHub Actions | Yes | .github/workflows/lint.yml | Workflow name: Lint |
| Docs | GitHub Actions | Yes | .github/workflows/docs.yml | Workflow name: Docs |
| Release | GitHub / Shields | Yes | Releases page | Only if releases exist |
| Issues | Shields.io | Yes | GitHub issues | Repo slug |
| Pull requests | Shields.io | Yes | GitHub PRs | Repo slug |

Coverage and code-quality badges are not included unless the repository produces and publishes them (e.g. via a workflow that uploads to a supported service).

## Scholarly Badges (Deferred Until Real Identifier)

- **Zenodo DOI**: Add to README only after reserving or publishing on Zenodo. See docs/zenodo-release.md and docs/doi-checklist.md. Placeholder: do not show in README until DOI is set.
- **arXiv**: Do not show in README until a real arXiv identifier (e.g. 24XX.XXXXX) is assigned. A template snippet for future activation is kept in this section, not in the live README.

### Template for arXiv Badge (Do Not Use Until Identifier Assigned)

When a preprint is submitted and an identifier is assigned, add to the README badge block:

```markdown
[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
```

Replace XXXX.XXXXX with the actual identifier. See docs/preprint-checklist.md.

## Validation

- Run `make verify-badges` or `python scripts/verify_badges.py` to check that every visible badge image and link URL resolves.
- CI may run badge verification; see .github/workflows if a dedicated job is added.
- Duplicate badges (same image or same link) should be avoided.

## Updating Badges

1. Edit README.md badge block only with URLs that you have verified (e.g. open in browser, or run verify_badges.py).
2. When adding a new workflow, add the corresponding badge using the workflow file name (e.g. `ci.yml` -> badge branch usually `main` or `develop`).
3. When a Zenodo DOI or arXiv ID is obtained, update README and this inventory, then run verify_badges.

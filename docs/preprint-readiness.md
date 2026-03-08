# Preprint Readiness

This document prepares the repository for a future arXiv (or equivalent) preprint that describes IRIDIUM. No preprint content or identifier is fabricated here.

## Purpose

When a paper is written and submitted, the repository should be in a state that supports:

- Clear citation of the software (via Zenodo DOI or release tag).
- Reproducibility of experiments (code version, environment, data provenance).
- Consistent notation and terminology with the paper (see docs/math-style-guide.md and docs/symbol-glossary.md).

## Repository State for Submission

- A release (or tag) should be cut that corresponds to the version used in the paper. That release should be archived on Zenodo so a DOI is available.
- CITATION.cff and .zenodo.json should list the correct version and authors.
- The paper should reference the software with "IRIDIUM, version X.Y.Z, https://github.com/iridium-oss/iridium (or Zenodo DOI)."

## arXiv Badge

Do not add an arXiv badge to the README until a real arXiv identifier (e.g. 24XX.XXXXX) has been assigned. When it has been assigned, add the badge using the template in docs/badges.md and run `make verify-badges`. See docs/preprint-checklist.md for the full checklist.

## Paper Assets

Figures, tables, and supplementary material that will accompany the preprint can be prepared under docs/paper-assets or a dedicated directory; see docs/paper-assets.md and docs/figures-and-tables-plan.md. Do not invent figure numbers or captions that imply a paper already exists.

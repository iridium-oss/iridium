# Release Checklist

Use this checklist when cutting a new release of IRIDIUM.

| Step | Owner | Blocking dependency | Completion criterion |
|------|--------|---------------------|----------------------|
| Bump version | Maintainer | None | pyproject.toml, CITATION.cff, .zenodo.json updated to new version |
| CHANGELOG | Maintainer | None | CHANGELOG.md has entry for this release with date and summary |
| CITATION.cff | Maintainer | Version | date-released set if known; version and url correct |
| Zenodo metadata | Maintainer | None | .zenodo.json version and description match release |
| DOI badge | Maintainer | Zenodo DOI assigned | If DOI exists, README badge added and verify-badges passes |
| README badge validation | CI or maintainer | None | make verify-badges passes |
| Docs validation | Maintainer | None | No broken internal links; docs/ and key paths reviewed |
| Provider matrix | Maintainer | None | docs/provider-matrix.md reflects current provider status |
| Tag and GitHub release | Maintainer | All above | Git tag created; GitHub release created with notes |
| Zenodo archival | Automatic | GitHub-Zenodo linked | New release triggers Zenodo ingest; DOI appears after processing |

Not all steps are blocking for every release (e.g. DOI badge only after first Zenodo archive). Document any skipped step and reason.

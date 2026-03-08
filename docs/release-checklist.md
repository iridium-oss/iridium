# Release Checklist

Use this checklist when cutting a new release of IRIDIUM.

| Step | Owner | Blocking dependency | Completion criterion |
|------|--------|---------------------|----------------------|
| Bump version | Maintainer | None | pyproject.toml and CITATION.cff updated to new version |
| CHANGELOG | Maintainer | None | CHANGELOG.md has entry for this release with date and summary |
| CITATION.cff | Maintainer | Version | date-released set if known; version and url correct |
| DOI badge | Maintainer | None | README badge present and valid |
| README badge validation | CI or maintainer | None | make verify-badges passes |
| Docs validation | Maintainer | None | No broken internal links; docs/ and key paths reviewed |
| Provider matrix | Maintainer | None | docs/provider-matrix.md reflects current provider status |
| Tag and GitHub release | Maintainer | All above | Git tag created; GitHub release created with notes |
| Zenodo archival | Automatic | GitHub-Zenodo linked | New release triggers Zenodo ingest; DOI appears after processing |

Not all steps are blocking for every release. Document any skipped step and reason.

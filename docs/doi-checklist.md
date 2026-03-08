# DOI Checklist

Use this when reserving or publishing a Zenodo DOI for IRIDIUM.

| Step | Completion criterion |
|------|----------------------|
| Zenodo account | Account created; GitHub account linked. |
| Enable repository | In Zenodo, enable archiving for iridium-oss/iridium. |
| First release | Create a GitHub release (tag + release notes). Zenodo will ingest it and assign a DOI. |
| Note DOI | Copy the Zenodo DOI (e.g. 10.5281/zenodo.XXXXXXX). |
| Add DOI badge | Add Zenodo DOI badge to README badge block; see docs/zenodo-release.md. |
| Update docs | docs/badges.md inventory; docs/citation.md if needed. |
| Verify | make verify-badges passes. |

Do not add a DOI badge with a placeholder or fabricated DOI. If the repository has not yet been released on Zenodo, leave the badge out and document the activation step in docs/zenodo-release.md.

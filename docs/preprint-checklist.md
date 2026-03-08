# Preprint Checklist

Use this when preparing or submitting a preprint (e.g. arXiv) that describes IRIDIUM.

| Step | Completion criterion |
|------|----------------------|
| Final title | Title agreed; consistent in paper and repository references. |
| Author order | Author list and order finalised; match CITATION.cff if software is co-released. |
| Abstract | Abstract written; consistent with README and docs where relevant. |
| Figures | Figures finalised; sources/scripts documented (see docs/paper-assets.md). |
| Tables | Tables finalised; data or scripts for reproducibility noted. |
| References | Bibliography complete; software cited with version and Zenodo DOI if available. |
| Reproducibility appendix | Optional: code version, environment, and data access described. |
| Repository version | A release or tag cut that matches the paper; Zenodo DOI obtained. |
| Zenodo cross-reference | Paper cites software with Zenodo DOI; repository can cite paper once published. |
| arXiv badge | Only after arXiv identifier is assigned: add badge to README using template in docs/badges.md; run make verify-badges. |

Do not add an arXiv badge to the README until a real arXiv identifier (e.g. 24XX.XXXXX) has been assigned. See docs/preprint-readiness.md and docs/badges.md.

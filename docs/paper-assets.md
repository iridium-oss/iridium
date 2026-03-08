# Paper Assets

When a preprint or paper is prepared, assets (figures, tables, supplementary material) can be stored and versioned here or in a dedicated directory.

## Suggested Layout

- **Figures**: Diagrams (architecture, pipeline, results) in a standard format (e.g. PDF or SVG for vector, PNG for raster). Name by purpose (e.g. architecture.pdf, forecasting-pipeline.pdf) rather than by paper figure number until the paper is final.
- **Tables**: Source data or generated tables (e.g. evaluation metrics, ablation) as CSV or Markdown so they can be regenerated or cited.
- **Supplementary**: Code snippets, extended proofs, or extra results that will appear in an appendix or supplementary file.

## Rules

- Do not commit large binary assets (e.g. full model checkpoints) to the repository unless they are essential and documented. Prefer URLs or instructions to obtain them.
- All assets should be documented (what they show, how they were produced, script or command if applicable). See docs/figures-and-tables-plan.md for a planning table.

## Citation

If the paper is published or assigned an identifier, the repository can reference it (e.g. in README or CITATION.cff) and the arXiv/DOI badge can be activated as described in docs/badges.md and docs/preprint-checklist.md.

# arXiv Preprint Package

This folder holds the arXiv-ready source package for the IRIDIUM paper.

## Generated artifact

- **iridium_preprint_source.zip**: Created by `python scripts/package_arxiv.py` from the **paper/** directory (run from repo root or from paper/).

The zip contains:

- main.tex, abstract.tex
- metadata/authors.tex, metadata/acknowledgements.tex
- refs/references.bib
- sections/*.tex
- figures/*.pdf and figures/*.png (all that exist at package time)

## How to submit to arXiv

1. From **paper/**: run `python scripts/package_arxiv.py`.
2. Upload **arxiv/iridium_preprint_source.zip** to arXiv as the source.
3. Compile on arXiv with: **pdflatex** and **bibtex** (default). No custom class path needed; IEEEtran is available. No shell-escape or non-standard dependencies.

## Note

The zip is generated and may be omitted from version control (e.g. via .gitignore). Regenerate it before each submission or when the manuscript or figures change.

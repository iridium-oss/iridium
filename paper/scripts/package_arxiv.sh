#!/usr/bin/env bash
# Package arXiv-ready source zip. Run from repository root or paper/
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_DIR="$(dirname "$SCRIPT_DIR")"
ARXIV_DIR="$PAPER_DIR/arxiv"
ZIP_NAME="iridium_preprint_source.zip"
cd "$PAPER_DIR"
rm -f "$ARXIV_DIR/$ZIP_NAME"
mkdir -p "$ARXIV_DIR"
zip -r "$ARXIV_DIR/$ZIP_NAME" \
  main.tex \
  abstract.tex \
  metadata/authors.tex \
  metadata/acknowledgements.tex \
  sections/*.tex \
  refs/references.bib \
  figures/*.pdf figures/*.png 2>/dev/null || true
echo "Created $ARXIV_DIR/$ZIP_NAME"
echo "Contents should include: main.tex, abstract.tex, sections/, refs/references.bib, figures/."

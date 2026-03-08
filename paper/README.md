# IRIDIUM Academic Paper

This directory contains the full manuscript for the IRIDIUM platform, prepared for repository inclusion, local LaTeX compilation, and arXiv submission. The paper is framed as a **provenance-aware urban mobility platform** with digital twin assembly, multimodal analytics, and a federated learning pathway for Azerbaijani cities. Claims are aligned with the current evaluation (API semantics, source-status, latency, weather integration).

## Title

IRIDIUM: A Provenance-Aware Urban Mobility Platform for Digital Twin Assembly, Multimodal Analytics, and Federated Learning in Azerbaijani Cities.

## Structure

| Path | Description |
|------|-------------|
| **main.tex** | IEEE journal article entry point (IEEEtran class). |
| **abstract.tex** | Abstract (provenance-first, no synthetic substitution, honest scope). |
| **sections/** | Numbered section files: 00_notation, 01_introduction through 10_conclusion, appendix. |
| **figures/** | PDF or PNG figures. Required for build: fig1_latency, fig2_temperature, fig3_precipitation (see below). |
| **refs/references.bib** | BibTeX bibliography. |
| **metadata/** | authors.tex, acknowledgements.tex, paper_metadata.yaml. |
| **scripts/** | package_arxiv.py, build_paper.sh, validate_references.py, check_latex_sources.py, verify_figures.py. |
| **arxiv/** | arXiv-ready source zip (iridium_preprint_source.zip) created by scripts/package_arxiv.py. |
| **build/** | Build log and artifacts. |
| **assets/manifest.json** | Figure and table manifest for traceability. |

## How to Build Locally

1. Install a LaTeX distribution (TeX Live, MiKTeX) with IEEEtran, amsmath, graphicx, bibtex, siunitx, algorithm, algpseudocode.
2. From the **paper/** directory:
   ```bash
   pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
   ```
   Or run: `./scripts/build_paper.sh` (if executable).
3. Output: **main.pdf**. The repository version does not add a draft or arXiv watermark.

## Figures

The paper references three figures in **figures/** (no file extension in LaTeX; add .pdf or .png):

- **fig1_latency**: API response latency (violin plots and ECDF). Can be generated with the repo script when the API is running: from repo root, `python scripts/measure_api_latency.py --plot --count 50`. Without the API, `python scripts/measure_api_latency.py --dummy` produces a placeholder so the paper builds.
- **fig2_temperature**: 72-hour Baku vs Quba temperature (Open-Meteo).
- **fig3_precipitation**: 72-hour Baku precipitation (Open-Meteo).

Weather figures are generated from the Open-Meteo API; see assets/manifest.json for source. No synthetic series.

## How to Package for arXiv

From **paper/** directory:

```bash
python scripts/package_arxiv.py
```

Output: **arxiv/iridium_preprint_source.zip**. Upload to arXiv; compile with pdflatex + bibtex. No shell-escape or non-standard dependencies. See **arxiv/README.md** for contents and usage.

## Validation

- `python scripts/validate_references.py`: Check references.bib.
- `python scripts/check_latex_sources.py`: Check \input and \includegraphics paths.
- `python scripts/verify_figures.py`: Check that all referenced figures exist under figures/.

## What Is Intentionally Excluded

- No fabricated benchmarks, metrics, or synthetic results in the main path. The paper reports only what the repository supports: API behavior, data-status semantics, source-status composition, latency, and real weather integration.
- No arXiv identifier in the repo until the preprint is submitted and assigned.

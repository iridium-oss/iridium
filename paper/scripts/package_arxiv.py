"""
Package arXiv-ready source zip. Cross-platform. Run from paper/ or repo root.
"""
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
PAPER_DIR = SCRIPT_DIR
ARXIV_DIR = PAPER_DIR / "arxiv"
ZIP_NAME = "iridium_preprint_source.zip"

def main():
    ARXIV_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = ARXIV_DIR / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()
    to_add = [
        "main.tex",
        "abstract.tex",
        "metadata/authors.tex",
        "metadata/acknowledgements.tex",
        "refs/references.bib",
    ]
    to_add.extend((PAPER_DIR / "sections").glob("*.tex"))
    to_add.extend((PAPER_DIR / "figures").glob("*.pdf"))
    to_add.extend((PAPER_DIR / "figures").glob("*.png"))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in to_add:
            if isinstance(p, str):
                p = PAPER_DIR / p
            if p.exists():
                z.write(p, p.relative_to(PAPER_DIR))
    print(f"Created {zip_path}")
    return 0

if __name__ == "__main__":
    exit(main())

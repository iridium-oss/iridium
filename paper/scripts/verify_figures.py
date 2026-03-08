"""
Verify that all figures referenced in the paper exist and are non-empty.
"""
import re
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
FIG_DIR = PAPER / "figures"

def main():
    errors = []
    for f in (PAPER / "sections").glob("*.tex"):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"\\includegraphics.*?\{([^}]+)\}", t):
            path = m.group(1).strip()
            base = path.replace("figures/", "").strip()
            for ext in ["", ".pdf", ".png"]:
                p = FIG_DIR / (base + ext)
                if p.exists():
                    if p.stat().st_size == 0:
                        errors.append(f"Empty figure: {p}")
                    break
            else:
                errors.append(f"Figure not found: {path}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("Figures OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())

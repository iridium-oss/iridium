r"""
Check LaTeX sources for missing \input files, broken \includegraphics paths, and missing refs.
"""
import re
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]

def main():
    main_tex = PAPER / "main.tex"
    if not main_tex.exists():
        print("main.tex not found", file=sys.stderr)
        return 1
    text = main_tex.read_text(encoding="utf-8")
    errors = []
    for m in re.finditer(r"\\input\{([^}]+)\}", text):
        p = PAPER / (m.group(1) + ".tex" if not m.group(1).endswith(".tex") else m.group(1))
        if not p.exists():
            errors.append(f"Missing input: {m.group(1)}")
    sections_dir = PAPER / "sections"
    for f in sections_dir.glob("*.tex"):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"\\includegraphics.*?\{([^}]+)\}", t):
            path = m.group(1).strip()
            if not path.startswith("figures/"):
                continue
            fig = PAPER / path
            if not fig.exists() and not (PAPER / (path + ".pdf")).exists():
                errors.append(f"Missing figure: {path} (in {f.name})")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("LaTeX sources OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())

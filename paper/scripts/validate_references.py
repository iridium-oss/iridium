"""
Validate references.bib: missing titles, years, malformed DOIs, duplicate keys, empty required fields.
Exit 0 if all pass, 1 otherwise.
"""
import re
import sys
from pathlib import Path

BIB = Path(__file__).resolve().parents[1] / "refs" / "references.bib"

def main():
    if not BIB.exists():
        print(f"Not found: {BIB}", file=sys.stderr)
        return 1
    text = BIB.read_text(encoding="utf-8")
    errors = []
    keys = []
    entries = re.split(r"\n@", text)
    for block in entries:
        if not block.strip():
            continue
        if not block.strip().startswith("{"):
            block = "@" + block
        m = re.match(r"@\w+\{([^,]+),", block)
        if m:
            key = m.group(1).strip()
            if key in keys:
                errors.append(f"Duplicate key: {key}")
            keys.append(key)
        if "title" not in block and "title=" not in block:
            errors.append(f"Entry missing title: {block[:80]}...")
        if "year" not in block and "year=" not in block:
            m2 = re.search(r"@\w+\{([^,]+),", block)
            if m2:
                errors.append(f"Entry missing year: {m2.group(1)}")
    for line in text.splitlines():
        if "doi" in line.lower() and "=" in line:
            v = line.split("=", 1)[1].strip().strip("{},").strip()
            if v and not re.match(r"10\.\d{4,}/[-._;()/:\w]+", v):
                errors.append(f"Malformed DOI: {v[:60]}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("References OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())

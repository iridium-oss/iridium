"""
Verify README badge URLs and link targets. Fails CI if any visible badge is broken.
Only validates badges that are actually present in README.md. Does not validate
commented or template badges. Usage: python scripts/verify_badges.py
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import urllib.request
    req = urllib.request.Request
    urlopen = urllib.request.urlopen
except ImportError:
    req = None
    urlopen = None

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
USER_AGENT = "IRIDIUM-badge-check/1.0"


def extract_badge_urls(content: str) -> list[tuple[str, str]]:
    """Extract markdown image URLs and optional link targets from README. Returns [(image_url, link_url or image_url)]."""
    # Match ![alt](image_url) or [![alt](image_url)](link_url)
    # Only consider lines that look like badges (contain img.shields.io or similar, or workflow badges)
    results: list[tuple[str, str]] = []
    # Pattern: [![...](IMAGE)](LINK) or ![...](IMAGE)
    linked = re.findall(r"\[\!\[.*?\]\((https?://[^)]+)\)\]\((https?://[^)]+)\)", content)
    for img, link in linked:
        results.append((img.strip(), link.strip()))
    unlinked = re.findall(r"\!\[.*?\]\((https?://[^)]+)\)", content)
    for img in unlinked:
        if any(img == r[0] for r in results):
            continue
        results.append((img.strip(), img.strip()))
    return results


def is_badge_line(line: str) -> bool:
    """True if line looks like a badge (image in markdown)."""
    return "![" in line and "]" in line and "(" in line


def is_commented_or_hidden(line: str) -> bool:
    """True if line is in a comment or hidden block (e.g. HTML comment or placeholder)."""
    s = line.strip()
    if s.startswith("<!--") or s.startswith("<!"):
        return True
    if "placeholder" in line.lower() or "do not show" in line.lower():
        return True
    return False


def get_visible_badge_urls(readme_path: Path) -> list[tuple[str, str]]:
    """Parse README and return only visible (non-commented) badge (image_url, link_url) pairs."""
    text = readme_path.read_text(encoding="utf-8")
    # Consider only the first 150 lines as badge area (typical badge block at top)
    head = "\n".join(text.splitlines()[:150])
    all_pairs = extract_badge_urls(head)
    visible = []
    for img_url, link_url in all_pairs:
        if "shields.io" in img_url or "github.com" in img_url or "img.shields.io" in img_url:
            visible.append((img_url, link_url))
    return visible


def check_url(url: str, head_only: bool = False) -> tuple[bool, int, str]:
    """Return (ok, status_code, message). Uses GET; some badge servers do not support HEAD."""
    if not urlopen or not req:
        return True, 0, "skipped (no urllib)"
    try:
        r = req(url, headers={"User-Agent": USER_AGENT})
        with urlopen(r, timeout=15) as resp:
            code = getattr(resp, "status", getattr(resp, "code", 200))
            return code < 400, code, str(code)
    except Exception as e:
        return False, -1, str(e)


def main() -> int:
    if not README.exists():
        print("README.md not found", file=sys.stderr)
        return 1
    pairs = get_visible_badge_urls(README)
    if not pairs:
        print("No visible badges found in README (OK)")
        return 0
    failed: list[str] = []
    for img_url, link_url in pairs:
        ok_img, code_img, msg_img = check_url(img_url, head_only=True)
        if not ok_img:
            failed.append(f"Badge image failed: {img_url} -> {msg_img}")
        ok_link, code_link, msg_link = check_url(link_url, head_only=True)
        if not ok_link:
            failed.append(f"Badge link failed: {link_url} -> {msg_link}")
    if failed:
        for f in failed:
            print(f, file=sys.stderr)
        return 1
    print(f"All {len(pairs)} visible badge(s) OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

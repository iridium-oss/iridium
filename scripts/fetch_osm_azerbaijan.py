"""
Fetch OpenStreetMap Azerbaijan extract from Geofabrik.
Records source timestamp and checksum. Raw PBF is not committed to git.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Geofabrik Europe Azerbaijan PBF (check URL for current)
GEOFABRIK_AZERBAIJAN = "https://download.geofabrik.de/europe/azerbaijan-latest.osm.pbf"
MANIFEST_FILENAME = "manifest.json"


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / "infrastructure" / "raw-sources" / "osm"
    out_dir.mkdir(parents=True, exist_ok=True)
    pbf_path = out_dir / "azerbaijan-latest.osm.pbf"

    try:
        import urllib.request
        req = urllib.request.Request(GEOFABRIK_AZERBAIJAN)
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = resp.read()
    except Exception as e:
        print(f"Fetch failed: {e}", file=sys.stderr)
        sys.exit(1)

    pbf_path.write_bytes(data)
    checksum = hashlib.sha256(data).hexdigest()
    fetched_at = datetime.now(timezone.utc).isoformat()

    manifest = {
        "source_name": "Geofabrik Azerbaijan",
        "source_url": GEOFABRIK_AZERBAIJAN,
        "fetched_at": fetched_at,
        "file_checksum_sha256": checksum,
        "file_path": str(pbf_path.relative_to(repo_root)),
        "license": "ODbL",
    }
    manifest_path = out_dir / MANIFEST_FILENAME
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Fetched {len(data)} bytes to {pbf_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()

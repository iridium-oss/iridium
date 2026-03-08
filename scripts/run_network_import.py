"""
Run network-import: load OSM PBF into PostgreSQL.
Requires: fetch_osm_azerbaijan.py run first, Postgres with schema applied, POSTGRES_* or POSTGRES_DSN set.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "services" / "network-import"))

from network_import.osm_to_network import main

if __name__ == "__main__":
    sys.exit(main())

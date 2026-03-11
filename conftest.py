"""Repo-root pytest config. Ensures earth-observation service is on path for EO tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parent
eo_service = root / "services" / "earth-observation"
if eo_service.exists() and str(eo_service) not in sys.path:
    sys.path.insert(0, str(eo_service))

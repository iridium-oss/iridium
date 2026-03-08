"""
IRIDIUM API entrypoint. Add service paths for in-repo imports.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for sub in (
    "services/digital-twin",
    "services/forecasting",
    "services/routing",
    "services/equity",
    "services/anomaly-detection",
    "services/ingestion",
    "services/weather-ingestion",
    "services/traffic-provider",
    "services/transit-ingestion",
    "services/network-import",
):
    p = ROOT / sub
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from app.application import create_app

app = create_app()

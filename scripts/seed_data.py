"""
Seed or generate sample data for local development.
Uses data/synthetic and optionally creates additional fixtures.
All data is synthetic; no real personal or operational data.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_SYNTHETIC = REPO_ROOT / "data" / "synthetic"
DATA_SAMPLES = REPO_ROOT / "data" / "samples"


def ensure_dirs() -> None:
    DATA_SYNTHETIC.mkdir(parents=True, exist_ok=True)
    DATA_SAMPLES.mkdir(parents=True, exist_ok=True)


def run_ingestion() -> None:
    """Run ingestion pipeline on synthetic data and print count."""
    sys.path.insert(0, str(REPO_ROOT))
    sys.path.insert(0, str(REPO_ROOT / "services" / "ingestion"))
    from ingestion.pipeline import run_ingestion as do_ingestion
    count, errors = do_ingestion(DATA_SAMPLES, DATA_SYNTHETIC)
    print(f"Ingestion: {count} records processed.")
    if errors:
        for e in errors[:10]:
            print(f"  Warning: {e}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more.")


def main() -> None:
    ensure_dirs()
    if not (DATA_SYNTHETIC / "sensor_events.json").exists():
        print("Synthetic data already present; skipping generation.")
    run_ingestion()
    print("Seed complete. Use data/synthetic and data/samples for demos.")


if __name__ == "__main__":
    main()

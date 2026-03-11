"""
Run federated learning simulation: generate partitions, then run Flower simulation.

Usage:
  cd services/forecasting/federated && python scripts/run_simulation.py
  Or: python -m federated.scripts.run_simulation (from federated dir)

Requires flwr[simulation]. Partitions are written to artifacts/partitions by default.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add federated package to path when run as script
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ARTIFACTS = ROOT / "artifacts"
PARTITIONS_DIR = ARTIFACTS / "partitions"


def main() -> int:
    from federated.partitioning import PartitionStrategy, generate_partitions
    from federated.task import get_model_input_dim

    PARTITIONS_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating partitions (by_district, simulation)...")
    manifests = generate_partitions(
        strategy=PartitionStrategy.BY_DISTRICT,
        num_partitions=3,
        samples_per_partition=100,
        feature_dim=get_model_input_dim(),
        seed=42,
        output_dir=PARTITIONS_DIR,
    )
    print(f"Generated {len(manifests)} partitions in {PARTITIONS_DIR}")
    for m in manifests:
        print(f"  {m.partition_id}: samples={m.sample_count}")

    # Run Flower simulation if flwr is available
    try:
        from federated.client_app import client_fn
        from federated.server_app import server_fn
        from flwr.client.client_app import ClientApp
        from flwr.serverapp import ServerApp
        from flwr.simulation import run_simulation
    except ImportError as e:
        print("Flower not available. Install with: pip install 'flwr[simulation]'")
        print("Partitions are ready. From federated dir run: flwr run .")
        print(str(e))
        return 0

    server_app = ServerApp(server_fn=server_fn)
    client_app = ClientApp(client_fn=client_fn)
    print("Starting Flower simulation (3 nodes, 3 rounds)...")
    print("Set IRIDIUM_FL_data_dir to", PARTITIONS_DIR, "so clients load partition data.")
    run_simulation(
        server_app=server_app,
        client_app=client_app,
        num_supernodes=3,
    )
    print("Simulation finished.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

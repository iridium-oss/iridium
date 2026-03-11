"""
Measure API response latency for paper reproducibility.
Calls GET /health, GET /api/v1/network/graph, GET /api/v1/forecast/congestion
repeatedly and writes CSV of response times (ms). Optional: plot ECDF to figures/.
Usage: API must be running (e.g. uvicorn). From repo root:
  python scripts/measure_api_latency.py [--count 50] [--base http://127.0.0.1:8000] [--plot]
"""

import argparse
import csv
import os
import sys
import time
from pathlib import Path

try:
    import urllib.request
except ImportError:
    urllib = None  # type: ignore


def measure(url: str, count: int) -> list[float]:
    times_ms: list[float] = []
    for _ in range(count):
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(url, timeout=30) as _:
                pass
        except Exception:
            times_ms.append(-1.0)  # failure
            continue
        elapsed_ms = (time.perf_counter() - t0) * 1000
        times_ms.append(elapsed_ms)
    return times_ms


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure API latency for paper.")
    parser.add_argument("--count", type=int, default=50, help="Requests per endpoint")
    parser.add_argument(
        "--base",
        default=os.environ.get("IRIDIUM_API_BASE", "http://127.0.0.1:8000"),
        help="API base URL",
    )
    parser.add_argument("--plot", action="store_true", help="Plot ECDF to paper/figures/")
    parser.add_argument("--out", type=str, default="", help="Output CSV path (default: stdout)")
    parser.add_argument(
        "--dummy",
        action="store_true",
        help="Plot ECDF from dummy data (for build; run without --dummy for real data)",
    )
    args = parser.parse_args()

    if urllib is None:
        print("urllib required", file=sys.stderr)
        return 1

    base = args.base.rstrip("/")
    endpoints = [
        ("health", f"{base}/health"),
        ("network_graph", f"{base}/api/v1/network/graph"),
        ("forecast_congestion", f"{base}/api/v1/forecast/congestion"),
    ]

    rows: list[dict] = []
    if not args.dummy:
        for name, url in endpoints:
            times = measure(url, args.count)
            valid = [t for t in times if t >= 0]
            for i, t in enumerate(times):
                rows.append({"endpoint": name, "request": i + 1, "latency_ms": t if t >= 0 else ""})
            if valid:
                valid.sort()
                n = len(valid)
                median = valid[n // 2] if n else 0
                p95 = valid[int(0.95 * n)] if n else 0
                print(
                    f"{name}: median={median:.1f} ms, 95th={p95:.1f} ms (n={len(valid)})",
                    file=sys.stderr,
                )

        out_path = args.out or None
        if out_path:
            Path(out_path).parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["endpoint", "request", "latency_ms"])
                w.writeheader()
                w.writerows(rows)
        elif not args.plot:
            w = csv.DictWriter(sys.stdout, fieldnames=["endpoint", "request", "latency_ms"])
            w.writeheader()
            w.writerows(rows)

    if args.plot or args.dummy:
        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            print("matplotlib and numpy required for --plot", file=sys.stderr)
            return 0
        fig, ax = plt.subplots(figsize=(5, 3))
        if args.dummy:
            # Placeholder ECDFs from typical latency ranges (for paper build without API)
            np.random.seed(42)
            for name, (lo, hi) in [
                ("health", (1, 6)),
                ("network_graph", (30, 130)),
                ("forecast_congestion", (40, 160)),
            ]:
                valid = np.random.uniform(lo, hi, args.count)
                valid.sort()
                y = np.arange(1, len(valid) + 1) / len(valid)
                ax.step(valid, y, where="post", label=name)
        else:
            for name, url in endpoints:
                times = measure(url, args.count)
                valid = np.array([t for t in times if t >= 0], dtype=float)
                if len(valid) == 0:
                    continue
                valid.sort()
                n = len(valid)
                y = np.arange(1, n + 1) / n
                ax.step(valid, y, where="post", label=name)
        ax.set_xlabel("Latency (ms)")
        ax.set_ylabel("ECDF")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        paper_fig = Path(__file__).resolve().parents[1] / "paper" / "figures"
        paper_fig.mkdir(parents=True, exist_ok=True)
        fig.savefig(paper_fig / "latency_ecdf.pdf", bbox_inches="tight")
        plt.close(fig)
        print(f"Wrote {paper_fig / 'latency_ecdf.pdf'}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())

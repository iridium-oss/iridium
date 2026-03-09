"""
Build GTFS Static from unified transit snapshot.
Label: repository-generated from official and public sources. No operator-issued claim.
Generate only agency, routes, stops, shapes where data exists. Omit stop_times if timetable not defensible.
"""

import csv
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

GTFS_BUILD_LABEL = "Repository-generated from official and public sources. Not operator-issued."


def _write_agency(snapshot: dict, out_dir: Path) -> None:
    agencies = snapshot.get("agencies") or []
    path = out_dir / "agency.txt"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["agency_id", "agency_name", "agency_url", "agency_timezone"])
        for a in agencies:
            w.writerow([
                getattr(a, "agency_id", ""),
                getattr(a, "name", ""),
                getattr(a, "url", "") or "",
                getattr(a, "timezone", "") or "Asia/Baku",
            ])


def _write_routes(snapshot: dict, out_dir: Path) -> None:
    routes = snapshot.get("routes") or []
    path = out_dir / "routes.txt"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["route_id", "agency_id", "route_short_name", "route_long_name", "route_type"])
        for r in routes:
            w.writerow([
                getattr(r, "route_id", ""),
                getattr(r, "agency_id", ""),
                getattr(r, "short_name", "") or "",
                getattr(r, "long_name", "") or "",
                getattr(r, "route_type", "") or "3",
            ])


def _write_stops(snapshot: dict, out_dir: Path) -> None:
    stops = snapshot.get("stops") or []
    path = out_dir / "stops.txt"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["stop_id", "stop_name", "stop_lat", "stop_lon"])
        for s in stops:
            lat = getattr(s, "lat", None)
            lon = getattr(s, "lon", None)
            w.writerow([
                getattr(s, "stop_id", ""),
                getattr(s, "name", "") or "",
                str(lat) if lat is not None else "",
                str(lon) if lon is not None else "",
            ])


def _write_shapes(snapshot: dict, out_dir: Path) -> None:  # pragma: no cover
    shapes = snapshot.get("shapes") or []
    path = out_dir / "shapes.txt"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"])
        for p in shapes:
            w.writerow([
                getattr(p, "shape_id", ""),
                getattr(p, "lat", ""),
                getattr(p, "lon", ""),
                getattr(p, "sequence", 0),
            ])


def build_gtfs_static(
    snapshot: dict,
    output_dir: Optional[os.PathLike[str]] = None,
) -> Path:
    """
    Write GTFS Static files to output_dir. Only files with real data are written.
    No stop_times or trips if timetable is not available (no fabricated schedule).
    When output_dir is None, uses storage feed export directory.
    """
    if output_dir is not None:
        out = Path(output_dir)
    else:
        from transit_ingestion.storage import get_feed_export_dir
        out = get_feed_export_dir()
    out.mkdir(parents=True, exist_ok=True)

    _write_agency(snapshot, out)
    _write_routes(snapshot, out)
    _write_stops(snapshot, out)
    if snapshot.get("shapes"):  # pragma: no cover
        _write_shapes(snapshot, out)

    readme = out / "README.txt"
    readme.write_text(
        GTFS_BUILD_LABEL + "\n"
        "Generated at " + datetime.now(timezone.utc).isoformat() + " UTC.\n"
        "agency.txt, routes.txt, stops.txt: from normalized BakuBus (AYNA) and Baku Metro data.\n"
        "shapes.txt: from AYNA flowCoordinates where available.\n"
        "trips.txt and stop_times.txt are omitted when exact timetable is not available.\n",
        encoding="utf-8",
    )
    return out

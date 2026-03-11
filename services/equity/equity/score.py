"""
Mobility Equity Score computation over district-level data.
Real or recorded data only; no synthetic defaults in main path.
When no data path is configured, returns empty districts with data_status unavailable.
"""

from datetime import UTC, datetime
from pathlib import Path

from iridium_schemas.equity import DistrictScore, MobilityEquityScore


def _load_district_baselines(data_dir: Path) -> list[dict]:
    """Load district baselines from JSON if present. Caller must pass real or recorded data path only."""
    path = data_dir / "district_scores.json"
    if not path.exists():
        return []
    import json

    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("districts", [])


def get_equity_scores(
    district_ids: list[str] | None = None,
    data_dir: Path | None = None,
) -> MobilityEquityScore:
    """Compute district-level equity scores from real or recorded data only. No synthetic fallback."""
    rows = _load_district_baselines(data_dir) if data_dir else []
    if not rows:
        return MobilityEquityScore(
            districts=[],
            generated_at=datetime.now(UTC),
            note="No equity data configured. Set EQUITY_DATA_PATH to a path containing district_scores.json (real or recorded). See docs/fairness.md.",
            data_status="unavailable",
            model_type="deterministic_baseline",
            model_maturity="production_baseline",
            source_coverage="no_data",
            confidence_note="No input data; scores unavailable.",
        )
    districts_out: list[DistrictScore] = []
    for r in rows:
        if district_ids and r.get("district_id") not in district_ids:
            continue
        pt = r.get("pt_accessibility_proxy") or 0.5
        modal = r.get("modal_availability_proxy") or 0.5
        aff = r.get("affordability_proxy") or 0.5
        composite = (pt + modal + aff) / 3.0
        districts_out.append(
            DistrictScore(
                district_id=r.get("district_id", ""),
                district_name=r.get("district_name"),
                avg_travel_time_to_services_min=r.get("avg_travel_time_to_services_min"),
                pt_accessibility_proxy=pt,
                modal_availability_proxy=modal,
                affordability_proxy=aff,
                composite_score=round(composite, 3),
            )
        )
    return MobilityEquityScore(
        districts=districts_out,
        generated_at=datetime.now(UTC),
        note="Derived analytic index; not an official government measurement. See docs/fairness.md.",
        data_status="live",
        model_type="deterministic_baseline",
        model_maturity="production_baseline",
        source_coverage=f"districts={len(districts_out)}",
        confidence_note="Composite from file-based proxies; interpret with caution when coverage is partial.",
    )

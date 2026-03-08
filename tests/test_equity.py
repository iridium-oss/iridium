"""Equity score tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for p in ("packages/schemas", "services/equity"):
    path = root / p
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from equity.score import get_equity_scores


def test_equity_scores_default():
    data_dir = root / "data" / "synthetic"
    result = get_equity_scores(data_dir=data_dir if data_dir.exists() else None)
    assert result.districts is not None
    if result.data_status == "unavailable":
        assert len(result.districts) == 0
    else:
        assert len(result.districts) >= 1


def test_equity_scores_filter_districts():
    data_dir = root / "data" / "synthetic"
    result = get_equity_scores(district_ids=["d1", "d2"], data_dir=data_dir if data_dir.exists() else None)
    if result.data_status == "unavailable":
        assert result.districts == []
    else:
        assert all(d.district_id in ("d1", "d2") for d in result.districts)


def test_equity_composite_in_range():
    data_dir = root / "data" / "synthetic"
    result = get_equity_scores(data_dir=data_dir if data_dir.exists() else None)
    for d in result.districts:
        if d.composite_score is not None:
            assert 0 <= d.composite_score <= 1

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
    result = get_equity_scores()
    assert result.districts is not None
    assert len(result.districts) >= 1


def test_equity_scores_filter_districts():
    result = get_equity_scores(district_ids=["d1", "d2"])
    assert all(d.district_id in ("d1", "d2") for d in result.districts)


def test_equity_composite_in_range():
    result = get_equity_scores()
    for d in result.districts:
        if d.composite_score is not None:
            assert 0 <= d.composite_score <= 1

"""Registry validation tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from forecasting.registry import load_registry_metadata, validate_artifact


def test_validate_no_metadata():
    assert validate_artifact(None, ["e1"]) is False


def test_validate_inactive():
    assert validate_artifact({"maturity": "inactive"}, ["e1"]) is False


def test_validate_ok():
    assert validate_artifact({"maturity": "candidate"}, ["e1"]) is True

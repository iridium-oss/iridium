"""
Tests for config.py to reach 100% coverage.
"""

import pytest
from pathlib import Path
from app.config import Settings

def test_cors_origins_list():
    s = Settings(CORS_ORIGINS=" http://a.com , http://b.com ")
    assert s.cors_origins_list() == ["http://a.com", "http://b.com"]

    s2 = Settings(CORS_ORIGINS="")
    assert s2.cors_origins_list() == []

def test_data_paths():
    s = Settings(DATA_SAMPLES_DIR="samples", DATA_SYNTHETIC_DIR="synthetic")
    assert s.data_samples_path() == Path("samples")
    assert s.data_synthetic_path() == Path("synthetic")

def test_equity_data_path_missing(tmp_path):
    # Path provided but does not exist
    s = Settings(EQUITY_DATA_PATH=str(tmp_path / "missing.csv"))
    assert s.equity_data_path() is None

    # Empty path
    s2 = Settings(EQUITY_DATA_PATH="")
    assert s2.equity_data_path() is None

def test_equity_data_path_exists(tmp_path):
    p = tmp_path / "exists.csv"
    p.write_text("data")
    s = Settings(EQUITY_DATA_PATH=str(p))
    assert s.equity_data_path() == p.resolve()

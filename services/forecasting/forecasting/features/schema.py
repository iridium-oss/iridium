"""
Feature schema versioning and definitions. Single source of truth for training and inference.
"""

FEATURE_SCHEMA_VERSION = "v1"

FEATURE_NAMES = [
    "target_lag_1", "target_lag_2", "target_lag_3",
    "rolling_mean_3", "rolling_std_3",
    "hour_sin", "hour_cos", "dow_sin", "dow_cos",
]


def build_feature_schema(version: str = FEATURE_SCHEMA_VERSION) -> dict:
    """Return schema metadata for the given version."""
    if version != FEATURE_SCHEMA_VERSION:
        return {"version": version, "compatible": False, "names": []}
    return {
        "version": version,
        "compatible": True,
        "names": list(FEATURE_NAMES),
        "description": "Lags, rolling stats, time encoding.",
    }

"""
Feature engineering for forecasting. Deterministic, versioned schema.
Training and inference use the same transformations.
"""

from .schema import FEATURE_SCHEMA_VERSION, build_feature_schema
from .pipeline import build_features, FeatureCoverage

__all__ = ["FEATURE_SCHEMA_VERSION", "build_feature_schema", "build_features", "FeatureCoverage"]

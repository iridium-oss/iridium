"""
Feature engineering for forecasting. Deterministic, versioned schema.
Training and inference use the same transformations.
"""

from .pipeline import FeatureCoverage, build_features
from .schema import FEATURE_SCHEMA_VERSION, build_feature_schema

__all__ = ["FEATURE_SCHEMA_VERSION", "build_feature_schema", "build_features", "FeatureCoverage"]

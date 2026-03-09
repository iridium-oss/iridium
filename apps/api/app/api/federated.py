"""
Federated learning status and capabilities API.

Exposes whether FL is active, model family, secure aggregation, DP, partitioning,
and maturity. No fabricated performance or run results.
"""

from fastapi import APIRouter

router = APIRouter()

# Scope and maturity: FL is runnable in simulation only; not used for production inference.
FEDERATED_STATUS = {
    "active": False,
    "description": "Federated learning is implemented for simulation and institution-lab use. It is not used for production inference.",
    "model_family": "congestion_forecasting",
    "deployment_mode": "simulation",
    "maturity": "experimental",
}

FEDERATED_CAPABILITIES = {
    "plain_fl": True,
    "secure_aggregation": False,
    "differential_privacy": False,
    "secure_aggregation_and_dp": False,
    "partitioning_schemes": ["by_district", "by_provider", "by_source_family", "by_time_block", "synthetic_institution"],
    "strategies": ["FedAvg"],
}

FEDERATED_PRIVACY_STATUS = {
    "secure_aggregation_enabled": False,
    "differential_privacy_enabled": False,
    "note": "Plain FedAvg only in current runs. Secure aggregation and DP are optional and not enabled by default. No privacy guarantee is claimed.",
}


@router.get("/federated/status", summary="Federated learning status")
def get_federated_status() -> dict:
    """Return whether FL is active, model family, deployment mode, and maturity. No fake metrics."""
    return FEDERATED_STATUS


@router.get("/federated/capabilities", summary="Federated learning capabilities")
def get_federated_capabilities() -> dict:
    """Return capability matrix: plain FL, secure aggregation, DP, partitioning, strategies."""
    return FEDERATED_CAPABILITIES


@router.get("/federated/runs", summary="Federated run list")
def get_federated_runs() -> dict:
    """Return list of run IDs. No run results stored in API; return empty unless artifact store is wired."""
    return {"runs": [], "note": "Run metadata is stored in federated artifacts; API does not enumerate runs."}


@router.get("/federated/runs/{run_id}", summary="Federated run detail")
def get_federated_run(run_id: str) -> dict:
    """Return run detail by ID. No fabricated results."""
    return {"run_id": run_id, "found": False, "note": "Run metadata is in federated artifacts."}


@router.get("/federated/models", summary="Federated model list")
def get_federated_models() -> dict:
    """Return list of federated model identifiers. No fake models."""
    return {"models": [], "note": "Federated model artifacts are stored in services/forecasting/federated/artifacts."}


@router.get("/federated/privacy-status", summary="Federated privacy status")
def get_federated_privacy_status() -> dict:
    """Return whether secure aggregation and DP are enabled. No overclaiming."""
    return FEDERATED_PRIVACY_STATUS

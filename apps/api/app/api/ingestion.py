"""
Ingestion endpoint: accept event batches.
"""

from fastapi import APIRouter, HTTPException

from iridium_schemas.events import IngestionEventBatch
from ingestion.pipeline import validate_batch

router = APIRouter()


@router.post("/ingestion/events", summary="Submit ingestion event batch")
def post_ingestion_events(body: IngestionEventBatch) -> dict:
    """
    Validate and accept a batch of ingestion events. Baseline: validate only; no persistence.
    Raw personal data must not be included; GNSS/telemetry assumed aggregated or anonymised.
    """
    ok, errors = validate_batch(body)
    if not ok:
        raise HTTPException(status_code=400, detail={"validation_errors": errors})
    count = (
        len(body.sensor_events)
        + len(body.gnss_points)
        + len(body.weather)
        + len(body.public_events)
        + len(body.energy_signals)
    )
    return {"accepted": count, "message": "Batch validated; persistence planned."}

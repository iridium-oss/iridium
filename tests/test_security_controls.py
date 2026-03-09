import sys
from pathlib import Path

from fastapi.testclient import TestClient

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "apps" / "api"))

from app.main import app  # noqa: E402
from app.observability.redaction import REDACTED, redact_event_dict  # noqa: E402


client = TestClient(app)


def test_request_validation_error_is_sanitized():
    r = client.post(
        "/api/v1/routing/plan",
        json={
            "origin_lat": "not-a-float",
            "origin_lon": 49.8,
            "destination_lat": 40.5,
            "destination_lon": 49.9,
        },
    )
    assert r.status_code == 400
    payload = r.json()
    errs = payload["error"]["details"]["errors"]
    assert isinstance(errs, list)
    assert errs, "Expected at least one validation error"
    assert all("input" not in e for e in errs)
    assert all(set(e.keys()) <= {"loc", "msg", "type"} for e in errs)


def test_structlog_redaction_processor():
    ev = {
        "event": "test",
        "traffic_api_key": "abc",
        "Authorization": "Bearer xyz",
        "nested": {"postgres_password": "pw", "ok": "value"},
        "list": [{"token": "t1"}, {"safe": "s"}],
    }
    out = redact_event_dict(ev)
    assert out["traffic_api_key"] == REDACTED
    assert out["Authorization"] == REDACTED
    assert out["nested"]["postgres_password"] == REDACTED
    assert out["nested"]["ok"] == "value"
    assert out["list"][0]["token"] == REDACTED
    assert out["list"][1]["safe"] == "s"


from fastapi.testclient import TestClient

from app.main import app


def test_not_found_errors_use_standard_shape() -> None:
    with TestClient(app) as client:
        response = client.get("/devices/not-a-real-device")

    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "message": "Device 'not-a-real-device' was not found.",
    }


def test_sync_action_returns_dry_run_metadata() -> None:
    with TestClient(app) as client:
        response = client.post("/devices/dev-win-001/sync")

    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "queued"
    assert body["dry_run"] is True
    assert body["recommended_actions"] == []
    assert "timestamp" in body

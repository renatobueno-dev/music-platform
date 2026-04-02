"""Contract tests for the root and health endpoints."""

from fastapi.testclient import TestClient


def test_root_returns_api_running_message(client: TestClient) -> None:
    """Verify the root endpoint returns the expected status payload."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Music Platform API is running"}


def test_health_returns_ok_status(client: TestClient) -> None:
    """Verify the health endpoint reports the service as healthy."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

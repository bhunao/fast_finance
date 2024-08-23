"""Testing the API endpoints and the templates returned by Jinja"""
from fastapi.testclient import TestClient


def test_get_check_health(client: TestClient) -> None:
    response = client.get(
        "/check_health/",
    )
    assert response.status_code == 200


def test_get_app_state(client: TestClient) -> None:
    response = client.get(
        "/app_state/",
    )
    assert response.status_code == 200
    state = response.json()["_state"]
    assert state["database_connection"] == True, "Database not connected."

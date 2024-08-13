"""Testing the API endpoints and the templates returned by Jinja"""
from fastapi.testclient import TestClient


def test_check_health(client: TestClient) -> None:
    response = client.get(
        "/check_health/",
    )
    assert response.status_code == 200

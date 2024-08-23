"""Testing the API endpoints and the templates returned by Jinja"""
from fastapi.testclient import TestClient
import pytest


def create_transaction(client: TestClient):
    body = {
        "external_id": 999,
        "value": 777,
        "type": "type_test",
        "destiny": "destiny_test",
        "description": "description_test"
    }
    response = client.post(
        "/transactions",
        json=body
    )
    return response.json()


def test_create_transaction(client: TestClient):
    body = {
        "external_id": 999,
        "value": 777,
        "type": "type_test",
        "destiny": "destiny_test",
        "description": "description_test"
    }
    response = client.post(
        "/transactions",
        json=body
    )

    assert response.status_code == 200

    json = response.json()
    del json["id"]

    assert json == body


def test_get_one_transaction(client: TestClient):
    created_json = create_transaction(client)
    response = client.get(
        f"/transactions/{created_json['id']}",
    )

    assert response.status_code == 200
    assert response.json() == created_json


def test_update_one_transaction(client: TestClient):
    created_json = create_transaction(client)

    body = {
        "id": created_json["id"],
        "description": "a new description to be there."
    }
    assert body["description"] != created_json["description"], "Values should be different before updating."
    response = client.patch(
        f"/transactions/{created_json['id']}",
        json=body
    )

    assert response.status_code == 200

    json = response.json()
    assert json["id"] == body["id"]
    assert json["description"] == body["description"]


def test_delete_one_transaction(client: TestClient):
    created_json = create_transaction(client)
    response = client.delete(
        f"/transactions/{created_json['id']}",
    )

    assert response.status_code == 200

    json = response.json()
    assert json["id"] == created_json["id"]


@pytest.mark.skip("Database mock is not working, the tests are saving on postgresql instead of sqlite.")
def test_get_all_transactions(client: TestClient) -> None:
    transactions_json_list = [create_transaction(client) for _ in range(10)]
    response = client.get(
        "/transactions/all",
    )

    assert response.status_code == 200

    json = response.json()
    assert len(json) == len(transactions_json_list)
    assert json == transactions_json_list

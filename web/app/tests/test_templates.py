"""Testing the API endpoints and the templates returned by Jinja"""
import pytest

from jinja2.environment import Template
from fastapi.testclient import TestClient
from httpx import Response

from app.models import Transaction


class TemplateResponse(Response):
    template: Template = Template("")


def has_template(response: TemplateResponse):
    assert hasattr(response, "template")
    assert isinstance(response.template, Template)
    assert hasattr(response, "context")
    assert isinstance(response.context, dict)
    return True


def test_transaction_all(client: TestClient):
    response: TemplateResponse = client.get(  # pyright: ignore[reportAssignmentType]
        "/web/transactions/all",
    )
    assert response.status_code == 200
    assert has_template(response)
    assert response.template.name == "table.html"

    rows = response.context["rows"]
    assert isinstance(rows, tuple)
    assert isinstance(rows[0], dict)


# @pytest.mark.skip("TDD, have to create the endpoint.")
def test_transaction_dashboard(client: TestClient):
    response: TemplateResponse = client.get(  # pyright: ignore[reportAssignmentType]
        "/web/transactions/dashboard",
    )
    assert response.status_code == 200
    assert has_template(response)
    assert response.template.name == "dashboard.html"

    rows = response.context["rows"]
    assert isinstance(rows, list)
    assert isinstance(rows[0], dict)


# test for the endpoint creatina.
def test_transaction_create(client: TestClient):
    response: TemplateResponse = client.get(  # pyright: ignore[reportAssignmentType]
        "/web/transactions/create",
    )
    assert response.status_code == 200
    assert has_template(response)
    assert response.template.name == "create.html"

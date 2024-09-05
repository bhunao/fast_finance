
"""Testing the API endpoints and the templates returned by Jinja"""
from jinja2.environment import Template
from fastapi.testclient import TestClient
from httpx import Response


class TemplateResponse(Response):
    template: Template = Template("")


def test_transaction_all(client: TestClient):
    response: TemplateResponse = client.get(  # pyright: ignore[reportAssignmentType]
        "/transactions/web/all",
    )

    assert response.status_code == 200
    assert response.template
    assert isinstance(response.template, Template)


def test_transaction_dashboard(client: TestClient):
    response: TemplateResponse = client.get(  # pyright: ignore[reportAssignmentType]
        "/transactions/web/dashboard",
    )
    assert response.status_code == 200
    assert response.template
    assert isinstance(response.template, Template)

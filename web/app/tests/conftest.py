import pytest

from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from app.core.database import get_session
from app.main import app, SQLModel


sqlite_url = "sqlite:///./db_test.db"
engine = create_engine(
    sqlite_url,
    echo=False,
    connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(engine)


def mock_get_session():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Fixture to create teste cliente per module."""
    app.dependency_overrides[get_session] = mock_get_session
    with TestClient(app) as client:
        yield client

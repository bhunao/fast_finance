from collections.abc import AsyncIterator
import logging

from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from types import AsyncGeneratorType
from typing import TypedDict

from fastapi import FastAPI, Request
from httpx import AsyncClient

from app.core.config import engine, settings
from app.models import SQLModel


log_format = (
    "[%(asctime)s | %(name)s | %(levelname)s | "
    "%(filename)s:%(lineno)d | %(funcName)s]: %(message)s"
)
logging.basicConfig(format=log_format, level=logging.INFO)


class State(TypedDict):
    database_connection: bool
    database_connection_error: Exception | None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    state = {
        "database_connection": False,
        "database_connection_error": None,
    }

    try:
        SQLModel.metadata.create_all(engine)
        state["database_connection"] = True
    except Exception as connection_error:
        state["database_connection_error"] = connection_error

    yield state


app = FastAPI(
    lifespan=lifespan
)


@app.get("/check_health")
async def check_health(r: Request):
    """Endpoint for testing if the web server is online."""
    return {"state": r.state}


@app.get("/app_state")
async def app_state(request: Request):
    """Get all the app state data."""
    return request.state

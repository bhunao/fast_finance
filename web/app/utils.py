from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, contextmanager
from typing import TypedDict

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Request
from sqlmodel import select

from app.core.database import get_session


def is_hx_request(request: Request):
    return request.headers.get("Hx-Request") == "true"


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


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
        with contextmanager(get_session)() as session:
            query = select(1)
            _ = session.exec(query).all()
        # run_migrations()
        state["database_connection"] = True
    except Exception as connection_error:
        # TODO: theres some typing issue here, i don't know which but its here
        state["database_connection_error"] = connection_error

    yield state

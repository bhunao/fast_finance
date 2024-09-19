from typing import Any
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, contextmanager
from typing import TypedDict
from io import StringIO

import pandas as pd

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Request, UploadFile
from sqlmodel import select
from pydantic.fields import FieldInfo

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

def get_input_type_from_field(field: FieldInfo) -> str:
    annotation = field.annotation
    if annotation is int:
        return "number"
    if annotation is float:
        return "number"
    if annotation is str:
        return "text"
    if annotation is bool:
        return "checkbox"
    return "text"

async def csv_file_to_dict(file: UploadFile) -> list[dict[str, Any]]:
    file = await file.read()
    string = str(file, "utf-8")
    io = StringIO(string)
    csv = pd.read_csv(io)
    result_ditct = csv.to_dict("records")
    return result_ditct

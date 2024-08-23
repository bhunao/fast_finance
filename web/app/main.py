from collections.abc import AsyncIterator
import logging

from contextlib import asynccontextmanager
from typing import TypedDict

from fastapi import FastAPI, Request

from app.core.config import settings
from app.core.database import engine
from app.models import SQLModel
from app.routers.transactions import router as transactions


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
        # TODO: theres some typing issue here, i don't know which but there is
        state["database_connection_error"] = connection_error

    yield state


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.include_router(transactions, prefix="/transactions")


@app.get("/check_health")
async def check_health(r: Request):
    """Endpoint for testing if the web server is online."""
    return r.state

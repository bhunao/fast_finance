from collections.abc import AsyncIterator
import logging

from contextlib import asynccontextmanager, contextmanager
from typing import TypedDict

from fastapi import FastAPI, Request
from sqlmodel import select
from alembic import command
from alembic.config import Config

from app.core.config import settings
from app.core.database import get_session
from app.routers.transactions import router as transactions


log_format = (
    "[%(asctime)s | %(name)s | %(levelname)s | "
    "%(filename)s:%(lineno)d | %(funcName)s]: %(message)s"
)
# logging.basicConfig(format=log_format, level=logging.INFO)
log = logging.getLogger("uvicorn")


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    log.info("Running alembic upgrade to head.")
    command.upgrade(alembic_cfg, "head")


class State(TypedDict):
    database_connection: bool
    database_connection_error: Exception | None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    log.info("Starting lifespan event.")
    state = {
        "database_connection": False,
        "database_connection_error": None,
    }

    try:
        with contextmanager(get_session)() as session:
            query = select(1)
            _ = session.exec(query).all()
        run_migrations()
        state["database_connection"] = True
    except Exception as connection_error:
        # TODO: theres some typing issue here, i don't know which but its here
        state["database_connection_error"] = connection_error

    yield state

    log.info("Ending lifespan event.")


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.include_router(transactions, prefix="/transactions")


@app.get("/check_health")
async def check_health(r: Request):
    """Endpoint for testing if the web server is online."""
    print(r.state.__dict__)
    return r.state

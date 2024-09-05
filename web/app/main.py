import logging

from typing import Any

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routers import transactions
from app.utils import is_hx_request, lifespan
# from app.utils import run_migrations


log_format = (
    "[%(asctime)s | %(name)s | %(levelname)s | "
    "%(filename)s:%(lineno)d | %(funcName)s]: %(message)s"
)
# logging.basicConfig(format=log_format, level=logging.INFO)
log = logging.getLogger("uvicorn")
TEMPLATES = settings.TEMPLATES.TemplateResponse


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.include_router(transactions.html_router, prefix="/web/transactions")
app.include_router(transactions.json_router, prefix="/json/transactions")

app.mount(
    "/static",
    StaticFiles(directory="static/"),
    name="static"
)


@app.get("/check_health")
async def check_health(r: Request):
    """Endpoint for testing if the web server is online."""
    print(r.state.__dict__)
    return r.state


@app.get("/")
async def readme(r: Request):
    context: dict[str, Any] = {
        "request": r,
        "title": "Readme",
    }

    return TEMPLATES(
        "readme.html",
        context=context,
        status_code=200,
        block_name="body" if is_hx_request(r) else None
    )


@app.get("/login")
async def login(r: Request):
    context: dict[str, Any] = {
        "request": r,
        "title": "Login",
    }

    return TEMPLATES(
        "login.html",
        context=context,
        status_code=200,
        block_name="body" if is_hx_request(r) else None
    )

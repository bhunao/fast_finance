import logging

from typing import Any
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.models import Transaction, TransactionCreate, TransactionUpdate


TEMPLATES = settings.TEMPLATES.TemplateResponse

logger = logging.getLogger(__name__)

html_router = APIRouter()
json_router = APIRouter()


class Context(BaseModel):
    request: Any  # error when `Request` is the type annotation
    title: str
    rows: Sequence[Transaction]
    table_index: bool = True


@json_router.post("/")
async def create(record: TransactionCreate, session: Session = Depends(get_session)):
    new_record = Transaction(**record.model_dump())

    session.add(new_record)
    session.commit()
    session.refresh(new_record)

    return new_record


@json_router.get("/all", response_model=list[Transaction])
async def get_all(session: Session = Depends(get_session)):
    statement = select(Transaction)
    result = session.exec(statement).all()
    return result


@json_router.get("/{id}", response_model=Transaction)
async def get_one(id: int, session: Session = Depends(get_session)):
    one = session.get_one(Transaction, id)
    return one


@json_router.patch("/{id}")
async def update(record: TransactionUpdate, session: Session = Depends(get_session)):
    _update = record.model_dump(exclude_none=True)
    one = False
    updated_record = False
    try:
        one = session.get_one(Transaction, record.id)
        updated_record = one.sqlmodel_update(_update)
        session.commit()
        session.refresh(one)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Trasanction with id '{record.id}' found."
        )

    return updated_record


@json_router.delete("/{id}")
async def delete(id: int, session: Session = Depends(get_session)):
    try:
        record = session.get_one(Transaction, id)
        session.delete(record)
        session.commit()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Trasanction with id '{id}' found."
        )
    return record


@html_router.get("/all", response_class=HTMLResponse)
async def home(request: Request, session: Session = Depends(get_session)):
    rows = session.exec(select(Transaction)).all()
    exclude_columns: set[str] = {"id"}

    def model_to_dict(rows: Sequence[Transaction], exclude: set[str] | None = None):
        exclude = exclude if exclude else set()
        rows = tuple(
            map(
                lambda r: r.model_dump(exclude=exclude),
                rows
            )
        )
        return rows

    context = Context(
        request=request,
        title="All Transactions",
        rows=model_to_dict(rows, exclude_columns)
    ).model_dump()

    is_hx_request = request.headers.get("Hx-Request") == "true"

    return TEMPLATES(
        "table.html",
        context=context,
        status_code=200,
        block_name="body" if is_hx_request else None
    )

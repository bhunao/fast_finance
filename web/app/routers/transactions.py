import logging

from typing import Any, DefaultDict, TypedDict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.models import Transaction, TransactionCreate, TransactionUpdate


TEMPLATES = settings.TEMPLATES.TemplateResponse
logger = logging.getLogger(__name__)
router = APIRouter()


class TemplateContext(TypedDict):
    request: Request
    title: str


@router.post("/")
async def create(record: TransactionCreate, session: Session = Depends(get_session)):
    new_record = Transaction(**record.model_dump())

    session.add(new_record)
    session.commit()
    session.refresh(new_record)

    return new_record


@router.get("/web/all")
async def home(request: Request, session: Session = Depends(get_session)):
    context: dict[str, Any] = {
        "request": request,
        "title": "All Transactions",
        "rows": session.exec(select(Transaction)).all(),
        # "include_fields": ["id", "value", "destiny"],
        # "exclude_fields": ["id", "value", "destiny"], # TODO: raise NotImplemented
        "table_index": True
    }

    is_hx_request = request.headers.get("Hx-Request") == "true"

    return TEMPLATES(
        "table.html",
        context=context,
        status_code=200,
        block_name="body" if is_hx_request else None
    )


@router.get("/all", response_model=list[Transaction])
async def get_all(session: Session = Depends(get_session)):
    statement = select(Transaction)
    result = session.exec(statement).all()
    return result


@router.get("/{id}", response_model=Transaction)
async def get_one(id: int, session: Session = Depends(get_session)):
    one = session.get_one(Transaction, id)
    return one


@router.patch("/{id}")
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


@router.delete("/{id}")
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

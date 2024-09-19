from typing import Annotated
from datetime import date

from sqlmodel import Field

from app.core.models import UserBase
from app.core.models import SQLModel as BaseModel
# from sqlmodel import SQLModel, Field

UserBase = UserBase


class TransactionFields:
    id = Annotated[int, Field(primary_key=True)]
    external_id = Annotated[str, Field(unique=True)]
    value = Annotated[int, Field()]
    date = Annotated[date, Field()]
    type = Annotated[str, Field()]
    destiny = Annotated[str, Field()]
    description = Annotated[str | None, Field(default=None)]


class TransactionUpdate(BaseModel):
    id: TransactionFields.id
    external_id: TransactionFields.external_id | None = None
    value: TransactionFields.value | None = None
    type: TransactionFields.type | None = None
    destiny: TransactionFields.destiny | None = None
    description: TransactionFields.description | None = None


class TransactionCreate(BaseModel):
    external_id: TransactionFields.external_id
    value: TransactionFields.value
    type: TransactionFields.type
    destiny: TransactionFields.destiny
    description: TransactionFields.description


class Transaction(BaseModel, table=True):
    id: TransactionFields.id
    date: TransactionFields.date
    type: TransactionFields.type
    destiny: TransactionFields.destiny
    value: TransactionFields.value
    external_id: TransactionFields.external_id
    description: TransactionFields.description

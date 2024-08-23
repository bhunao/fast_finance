from typing import Annotated

from app.core.models import UserBase
from app.core.models import SQLModel, Field

UserBase = UserBase


class TransactionFields:
    id = Annotated[int, Field(primary_key=True)]
    external_id = Annotated[int, Field()]
    value = Annotated[int, Field()]
    type = Annotated[str, Field()]
    destiny = Annotated[str, Field()]
    description = Annotated[str | None, Field(default=None)]


class TransactionUpdate(SQLModel):
    id: TransactionFields.id
    external_id: TransactionFields.external_id | None = None
    value: TransactionFields.value | None = None
    type: TransactionFields.type | None = None
    destiny: TransactionFields.destiny | None = None
    description: TransactionFields.description | None = None


class TransactionCreate(SQLModel):
    external_id: TransactionFields.external_id
    value: TransactionFields.value
    type: TransactionFields.type
    destiny: TransactionFields.destiny
    description: TransactionFields.description


class Transaction(SQLModel, table=True):
    id: TransactionFields.id
    external_id: TransactionFields.external_id
    value: TransactionFields.value
    type: TransactionFields.type
    destiny: TransactionFields.destiny
    description: TransactionFields.description

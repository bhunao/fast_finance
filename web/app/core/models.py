from typing import Annotated

from sqlmodel import SQLModel
from sqlmodel import Field


class UserFields:
    id = Annotated[int, Field(primary_key=True)]
    username = Annotated[str, Field(title="Usuário")]
    password = Annotated[str, Field(title="Senha")]


class UserBase(SQLModel, table=True):
    __tablename__ = "user"

    id: UserFields.id
    username: UserFields.username
    password: UserFields.password


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: int | None = None

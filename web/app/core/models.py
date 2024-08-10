from typing import Annotated

from pydantic import Field
from sqlmodel import SQLModel


class UserFields(SQLModel):
    id = Annotated[int, Field()]
    username = Annotated[str, Field(title="Usuário")]
    password = Annotated[str, Field(title="Senha")]


class UserBase(SQLModel):
    id: UserFields.id
    username: UserFields.username
    password: UserFields.password


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: int | None = None

from typing import Annotated

from pydantic import Field
from sqlmodel import SQLModel


class UserFields(SQLModel):
    username: Annotated[str, Field(title="Usuário")]
    password: Annotated[str, Field(title="Senha")]


class UserBase(SQLModel):
    username: UserFields.username
    password: UserFields.password

from pydantic.fields import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from jinja2_fragments.fastapi import Jinja2Blocks
from sqlmodel import create_engine


class Settings(BaseSettings):
    DATABASE_USER: str = "admin"
    DATABASE_PASSWORD: str = "1234"
    DATABASE_SERVER: str = "server"
    DATABASE_PORT: int = 8181
    DATABASE_DB: str = "projectdb"

    MONGO_INITDB_ROOT_USERNAME: str = "REPLACE"
    MONGO_INITDB_ROOT_PASSWORD: str = "REPLACE"

    TEMPLATES: Jinja2Blocks = Jinja2Blocks(directory="templates")

    @computed_field()
    @property
    def DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_SERVER,
            port=self.DATABASE_PORT,
            path=self.DATABASE_DB,
        )


settings = Settings()
engine = create_engine(str(settings.DATABASE_URI))

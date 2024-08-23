from pydantic.fields import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from jinja2_fragments.fastapi import Jinja2Blocks
from sqlmodel import create_engine


class Settings(BaseSettings):
    APP_NAME: str = "Fast Finance"

    DATABASE_USER: str = "DATABASE_USER"
    DATABASE_PASSWORD: str = "DATABASE_PASSWORD"
    DATABASE_SERVER: str = "DATABASE_SERVER"
    DATABASE_PORT: int = 9999
    DATABASE_DB: str = "DATABASE_DB"

    MONGO_INITDB_ROOT_USERNAME: str = "SECRETUSERNAME"
    MONGO_INITDB_ROOT_PASSWORD: str = "SECRETPASSWORD"

    TEMPLATES: Jinja2Blocks = Jinja2Blocks(directory="templates")

    @computed_field
    @property
    def DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_SERVER,
            port=self.DATABASE_PORT,
            path=self.DATABASE_DB,
        )


settings = Settings()

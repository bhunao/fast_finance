from collections.abc import Generator

from sqlmodel import Session, create_engine
from app.core.config import settings


engine = create_engine(str(settings.DATABASE_URI))


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

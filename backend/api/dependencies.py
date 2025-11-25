from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from database.database import engine


def get_database_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_database_session)]

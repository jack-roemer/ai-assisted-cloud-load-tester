from collections.abc import Generator
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase


DATABASE_PATH = Path("demo.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


engine = create_engine(
    DATABASE_URL,
    # in fastapi a single request can use different threads or multiple concurrent requests may need to access the database at the same time, so we disable the check for same thread in sqlite
    connect_args={"check_same_thread": False}, 
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


def get_db() -> Generator[Session, None, None]:
    """Provides a database session to API routes."""

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# better once the dependency is used in multiple routes
DBSessionDependency = Annotated[Session, Depends(get_db)]
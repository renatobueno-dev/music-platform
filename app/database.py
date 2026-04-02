"""Database engine and session helpers for the application runtime."""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session, sessionmaker


def validate_database_url(database_url: str) -> str:
    """Validate supported database URL schemes before engine creation."""
    try:
        parsed_url = make_url(database_url)
    except ArgumentError as exc:
        raise RuntimeError(
            "Invalid DATABASE_URL format. Use sqlite:///path/to.db or "
            "postgresql+psycopg://user:password@host:5432/database."
        ) from exc

    if not (
        parsed_url.drivername.startswith("sqlite") or parsed_url.drivername.startswith("postgresql")
    ):
        raise RuntimeError(
            f"Invalid DATABASE_URL scheme '{parsed_url.drivername}'. Use sqlite or postgresql."
        )

    return database_url


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required.")

DATABASE_URL = validate_database_url(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SESSION_FACTORY = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a request-scoped SQLAlchemy session and close it afterwards."""
    session = SESSION_FACTORY()
    try:
        yield session
    finally:
        session.close()

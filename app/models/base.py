"""Shared SQLAlchemy declarative base and reusable model helpers."""

from typing import Any

from sqlalchemy import inspect as inspect_model
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for every ORM model in the application."""

    def as_dict(self) -> dict[str, Any]:
        """Return mapped column values as a plain dictionary."""
        mapper = inspect_model(self).mapper
        return {column.key: getattr(self, column.key) for column in mapper.columns}

    def primary_key_values(self) -> tuple[Any, ...]:
        """Return the current mapped primary-key values in declared order."""
        mapper = inspect_model(self).mapper
        return tuple(getattr(self, column.key) for column in mapper.primary_key)

"""Alembic environment configuration for online and offline migrations."""

from __future__ import annotations

import os
from logging.config import fileConfig
from typing import Any

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.models import Base


def get_dynamic_member(obj: Any, attribute_name: str) -> Any:
    """Return a dynamic attribute from a proxy-style runtime object."""
    return getattr(obj, attribute_name)


config = get_dynamic_member(context, "config")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_database_url() -> str:
    """Return the DATABASE_URL required by Alembic execution."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is required to run Alembic migrations."
        )
    return database_url


def invoke_context_method(method_name: str, *args: Any, **kwargs: Any) -> Any:
    """Call an Alembic context method exposed through the runtime proxy."""
    return get_dynamic_member(context, method_name)(*args, **kwargs)


def run_migrations_offline() -> None:
    """Configure Alembic for offline SQL rendering."""
    invoke_context_method(
        "configure",
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with invoke_context_method("begin_transaction"):
        invoke_context_method("run_migrations")


def run_migrations_online() -> None:
    """Configure Alembic with a live database connection."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_database_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        invoke_context_method(
            "configure",
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with invoke_context_method("begin_transaction"):
            invoke_context_method("run_migrations")


if bool(invoke_context_method("is_offline_mode")):
    run_migrations_offline()
else:
    run_migrations_online()

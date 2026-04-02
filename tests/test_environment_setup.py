"""Tests that confirm the disposable database environment is active."""

from importlib import import_module
from pathlib import Path


def get_database_url() -> str:
    """Read the database URL exposed by the runtime database module."""
    database_module = import_module("app.database")
    return str(database_module.DATABASE_URL)


def test_test_database_url_uses_disposable_sqlite_environment() -> None:
    """Verify tests run against a disposable SQLite database path."""
    database_url = get_database_url()

    assert database_url.startswith("sqlite:///")
    assert "music-platform-tests-" in database_url

    db_path = Path(database_url.removeprefix("sqlite:///"))
    assert db_path.name == "test_contract.db"

from pathlib import Path


def test_test_database_url_uses_disposable_sqlite_environment() -> None:
    from app.database import DATABASE_URL

    assert DATABASE_URL.startswith("sqlite:///")
    assert "music-platform-tests-" in DATABASE_URL

    db_path = Path(DATABASE_URL.removeprefix("sqlite:///"))
    assert db_path.name == "test_contract.db"

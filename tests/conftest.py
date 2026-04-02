"""Pytest fixtures and disposable test-database bootstrap."""

import os
import shutil
import sys
import tempfile
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Keep test execution independent from local runtime database state.
TEST_RUN_DIR = Path(tempfile.mkdtemp(prefix="music-platform-tests-"))
TEST_DB_PATH = TEST_RUN_DIR / "test_contract.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
os.environ["STARTUP_DB_MAX_RETRIES"] = "1"
os.environ["STARTUP_DB_RETRY_SECONDS"] = "0"


def load_test_runtime() -> tuple[Any, Any, Any]:
    """Import runtime modules after the disposable environment is configured."""
    database_module = import_module("app.database")
    main_module = import_module("app.main")
    models_module = import_module("app.models")
    return (
        database_module.engine,
        main_module.app,
        models_module.Base,
    )


ENGINE, APP, BASE = load_test_runtime()


@pytest.fixture(autouse=True)
def reset_database() -> None:
    """Reset the database schema before every test case."""
    BASE.metadata.drop_all(bind=ENGINE)
    BASE.metadata.create_all(bind=ENGINE)
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_artifacts() -> None:
    """Dispose the engine and remove temporary files after the test session."""
    yield
    ENGINE.dispose()
    shutil.rmtree(TEST_RUN_DIR, ignore_errors=True)


@pytest.fixture
def client() -> TestClient:
    """Return a FastAPI test client bound to the disposable database."""
    with TestClient(APP) as test_client:
        yield test_client

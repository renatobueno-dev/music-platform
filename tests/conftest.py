import os
import shutil
import sys
import tempfile
from pathlib import Path

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

from app.database import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Base  # noqa: E402


@pytest.fixture(autouse=True)
def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_artifacts() -> None:
    yield
    engine.dispose()
    shutil.rmtree(TEST_RUN_DIR, ignore_errors=True)


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client

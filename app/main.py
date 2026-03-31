import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError

from app.database import engine
from app.routes.health import router as health_router
from app.routes.playlists import router as playlists_router
from app.routes.songs import router as songs_router

logger = logging.getLogger(__name__)
STARTUP_DB_MAX_RETRIES = int(os.getenv("STARTUP_DB_MAX_RETRIES", "20"))
STARTUP_DB_RETRY_SECONDS = float(os.getenv("STARTUP_DB_RETRY_SECONDS", "2"))
REQUIRED_TABLES = {"songs", "playlists", "playlist_songs"}


def wait_for_database() -> None:
    for attempt in range(1, STARTUP_DB_MAX_RETRIES + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            if attempt > 1:
                logger.info("Database became reachable on startup attempt %s.", attempt)
            return
        except OperationalError as exc:
            if attempt == STARTUP_DB_MAX_RETRIES:
                logger.exception(
                    "Database startup failed after %s attempts.",
                    STARTUP_DB_MAX_RETRIES,
                )
                raise
            logger.warning(
                "Database not ready on startup attempt %s/%s: %s. Retrying in %.1f seconds.",
                attempt,
                STARTUP_DB_MAX_RETRIES,
                exc,
                STARTUP_DB_RETRY_SECONDS,
            )
            time.sleep(STARTUP_DB_RETRY_SECONDS)


def validate_required_schema() -> None:
    inspector = inspect(engine)
    missing_tables = sorted(
        table_name for table_name in REQUIRED_TABLES if not inspector.has_table(table_name)
    )
    if missing_tables:
        raise RuntimeError(
            "Database schema is missing required tables: "
            f"{missing_tables}. Run migrations with: alembic upgrade head"
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    wait_for_database()
    validate_required_schema()
    yield


app = FastAPI(
    title="Music Platform API",
    version="1.6.1",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Music Platform API is running"}


app.include_router(health_router)
app.include_router(songs_router)
app.include_router(playlists_router)

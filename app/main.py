from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routes.health import router as health_router
from app.routes.playlists import router as playlists_router
from app.routes.songs import router as songs_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Music Platform API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Music Platform API is running"}


app.include_router(health_router)
app.include_router(songs_router)
app.include_router(playlists_router)

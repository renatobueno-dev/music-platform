from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.song import SongCreate, SongRead
from app.services.song_service import create_song, list_songs

router = APIRouter(prefix="/songs", tags=["songs"])


@router.get("/", response_model=list[SongRead])
def read_songs(session: Session = Depends(get_session)) -> list[SongRead]:
    return list_songs(session)


@router.post("/", response_model=SongRead, status_code=status.HTTP_201_CREATED)
def create_song_endpoint(
    payload: SongCreate,
    session: Session = Depends(get_session),
) -> SongRead:
    return create_song(session, payload)

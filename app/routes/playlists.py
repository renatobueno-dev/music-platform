from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.playlist import PlaylistCreate, PlaylistRead
from app.services.playlist_service import create_playlist, list_playlists

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.get("/", response_model=list[PlaylistRead])
def read_playlists(session: Session = Depends(get_session)) -> list[PlaylistRead]:
    return list_playlists(session)


@router.post("/", response_model=PlaylistRead, status_code=status.HTTP_201_CREATED)
def create_playlist_endpoint(
    payload: PlaylistCreate,
    session: Session = Depends(get_session),
) -> PlaylistRead:
    return create_playlist(session, payload)

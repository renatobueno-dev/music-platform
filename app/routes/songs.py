"""Song route definitions and HTTP error mapping."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.song import SongCreate, SongRead, SongUpdate
from app.services.song_service import (
    create_song,
    delete_song,
    get_song_by_id,
    list_songs,
    update_song,
)

router = APIRouter(prefix="/songs", tags=["songs"])


@router.get("/", response_model=list[SongRead])
def read_songs(session: Session = Depends(get_session)) -> list[SongRead]:
    """List persisted songs using the service-layer ordering rules."""
    return list_songs(session)


@router.post("/", response_model=SongRead, status_code=status.HTTP_201_CREATED)
def create_song_endpoint(
    payload: SongCreate,
    session: Session = Depends(get_session),
) -> SongRead:
    """Create one song from the validated request payload."""
    return create_song(session, payload)


@router.get("/{song_id}", response_model=SongRead)
def read_song(song_id: int, session: Session = Depends(get_session)) -> SongRead:
    """Return one song or translate a missing record into HTTP 404."""
    song = get_song_by_id(session, song_id)
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song


@router.patch("/{song_id}", response_model=SongRead)
def update_song_endpoint(
    song_id: int,
    payload: SongUpdate,
    session: Session = Depends(get_session),
) -> SongRead:
    """Apply partial updates to a song or return HTTP 404 when absent."""
    song = get_song_by_id(session, song_id)
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return update_song(session, song, payload)


@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_song_endpoint(song_id: int, session: Session = Depends(get_session)) -> Response:
    """Delete a song and return an empty successful response."""
    song = get_song_by_id(session, song_id)
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")

    delete_song(session, song)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

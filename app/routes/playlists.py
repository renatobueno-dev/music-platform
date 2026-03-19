from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.playlist import PlaylistCreate, PlaylistRead, PlaylistUpdate
from app.services.playlist_service import (
    create_playlist,
    delete_playlist,
    get_playlist_by_id,
    list_playlists,
    update_playlist,
)

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


@router.get("/{playlist_id}", response_model=PlaylistRead)
def read_playlist(playlist_id: int, session: Session = Depends(get_session)) -> PlaylistRead:
    playlist = get_playlist_by_id(session, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    return playlist


@router.patch("/{playlist_id}", response_model=PlaylistRead)
def update_playlist_endpoint(
    playlist_id: int,
    payload: PlaylistUpdate,
    session: Session = Depends(get_session),
) -> PlaylistRead:
    playlist = get_playlist_by_id(session, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    return update_playlist(session, playlist, payload)


@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist_endpoint(playlist_id: int, session: Session = Depends(get_session)) -> Response:
    playlist = get_playlist_by_id(session, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")

    delete_playlist(session, playlist)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.playlist import Playlist
from app.schemas.playlist import PlaylistCreate


def list_playlists(session: Session) -> list[Playlist]:
    statement = select(Playlist).order_by(Playlist.id)
    return list(session.scalars(statement).all())


def create_playlist(session: Session, payload: PlaylistCreate) -> Playlist:
    playlist = Playlist(**payload.model_dump())
    session.add(playlist)
    session.commit()
    session.refresh(playlist)
    return playlist

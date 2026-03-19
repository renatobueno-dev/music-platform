from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.playlist import Playlist
from app.schemas.playlist import PlaylistCreate, PlaylistUpdate


def list_playlists(session: Session) -> list[Playlist]:
    statement = select(Playlist).order_by(Playlist.id)
    return list(session.scalars(statement).all())


def create_playlist(session: Session, payload: PlaylistCreate) -> Playlist:
    playlist = Playlist(**payload.model_dump())
    session.add(playlist)
    session.commit()
    session.refresh(playlist)
    return playlist


def get_playlist_by_id(session: Session, playlist_id: int) -> Playlist | None:
    return session.get(Playlist, playlist_id)


def update_playlist(session: Session, playlist: Playlist, payload: PlaylistUpdate) -> Playlist:
    updates = payload.model_dump(exclude_unset=True)
    for field_name, value in updates.items():
        setattr(playlist, field_name, value)

    session.commit()
    session.refresh(playlist)
    return playlist


def delete_playlist(session: Session, playlist: Playlist) -> None:
    session.delete(playlist)
    session.commit()

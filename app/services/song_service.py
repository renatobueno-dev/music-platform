from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.song import Song
from app.schemas.song import SongCreate, SongUpdate


def list_songs(session: Session) -> list[Song]:
    statement = select(Song).order_by(Song.id)
    return list(session.scalars(statement).all())


def create_song(session: Session, payload: SongCreate) -> Song:
    song = Song(**payload.model_dump())
    session.add(song)
    session.commit()
    session.refresh(song)
    return song


def get_song_by_id(session: Session, song_id: int) -> Song | None:
    return session.get(Song, song_id)


def update_song(session: Session, song: Song, payload: SongUpdate) -> Song:
    updates = payload.model_dump(exclude_unset=True)
    for field_name, value in updates.items():
        setattr(song, field_name, value)

    session.commit()
    session.refresh(song)
    return song


def delete_song(session: Session, song: Song) -> None:
    session.delete(song)
    session.commit()

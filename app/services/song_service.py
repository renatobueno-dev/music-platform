from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.song import Song
from app.schemas.song import SongCreate


def list_songs(session: Session) -> list[Song]:
    statement = select(Song).order_by(Song.id)
    return list(session.scalars(statement).all())


def create_song(session: Session, payload: SongCreate) -> Song:
    song = Song(**payload.model_dump())
    session.add(song)
    session.commit()
    session.refresh(song)
    return song

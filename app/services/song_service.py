"""Song persistence helpers used by the route layer."""

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.song import Song
from app.schemas.song import SongCreate, SongUpdate

logger = logging.getLogger(__name__)


def list_songs(session: Session) -> list[Song]:
    """Return songs in a stable order for predictable API responses."""
    statement = select(Song).order_by(Song.id)
    songs = session.scalars(statement).all()
    logger.debug("Listed %s songs.", len(songs))
    return songs


def create_song(session: Session, payload: SongCreate) -> Song:
    """Persist a new song and return the refreshed ORM object."""
    song = Song(**payload.model_dump())
    session.add(song)
    session.commit()
    session.refresh(song)
    logger.info("Created song id=%s.", song.id)
    return song


def get_song_by_id(session: Session, song_id: int) -> Song | None:
    """Load a song by primary key or return ``None`` when missing."""
    return session.get(Song, song_id)


def update_song(session: Session, song: Song, payload: SongUpdate) -> Song:
    """Apply partial updates and return the refreshed song state."""
    updates = payload.model_dump(exclude_unset=True)
    for field_name, value in updates.items():
        setattr(song, field_name, value)

    session.commit()
    session.refresh(song)
    logger.info("Updated song id=%s with fields=%s.", song.id, sorted(updates))
    return song


def delete_song(session: Session, song: Song) -> None:
    """Delete a song and commit the change immediately."""
    song_id = song.id
    session.delete(song)
    session.commit()
    logger.info("Deleted song id=%s.", song_id)

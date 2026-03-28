from collections.abc import Sequence
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.playlist import Playlist
from app.models.song import Song
from app.schemas.playlist import PlaylistCreate, PlaylistUpdate

logger = logging.getLogger(__name__)


class MissingSongsError(Exception):
    def __init__(self, missing_song_ids: list[int]) -> None:
        self.missing_song_ids = missing_song_ids
        message = f"Songs not found: {missing_song_ids}"
        super().__init__(message)


def _deduplicate_ids(ids: Sequence[int]) -> list[int]:
    # Keep input order stable while removing duplicates.
    return list(dict.fromkeys(ids))


def _resolve_songs(session: Session, song_ids: Sequence[int]) -> list[Song]:
    unique_song_ids = _deduplicate_ids(song_ids)
    if not unique_song_ids:
        return []

    statement = select(Song).where(Song.id.in_(unique_song_ids))
    songs = session.scalars(statement).all()
    songs_by_id = {song.id: song for song in songs}
    missing_song_ids = [song_id for song_id in unique_song_ids if song_id not in songs_by_id]

    if missing_song_ids:
        logger.warning("Playlist operation aborted. Missing songs: %s.", missing_song_ids)
        raise MissingSongsError(missing_song_ids)

    return [songs_by_id[song_id] for song_id in unique_song_ids]


def list_playlists(session: Session) -> list[Playlist]:
    statement = select(Playlist).options(selectinload(Playlist.songs)).order_by(Playlist.id)
    playlists = session.scalars(statement).all()
    logger.debug("Listed %s playlists.", len(playlists))
    return playlists


def create_playlist(session: Session, payload: PlaylistCreate) -> Playlist:
    playlist_data = payload.model_dump(exclude={"song_ids"})
    playlist = Playlist(**playlist_data)
    playlist.songs = _resolve_songs(session, payload.song_ids)
    session.add(playlist)
    session.commit()
    created_playlist = get_playlist_by_id(session, playlist.id)
    if created_playlist is None:
        raise RuntimeError("Created playlist could not be reloaded")
    logger.info("Created playlist id=%s.", created_playlist.id)
    return created_playlist


def get_playlist_by_id(session: Session, playlist_id: int) -> Playlist | None:
    statement = (
        select(Playlist)
        .where(Playlist.id == playlist_id)
        .options(selectinload(Playlist.songs))
    )
    return session.scalar(statement)


def update_playlist(session: Session, playlist: Playlist, payload: PlaylistUpdate) -> Playlist:
    updates = payload.model_dump(exclude_unset=True, exclude={"song_ids"})
    original_playlist_id = playlist.id
    for field_name, value in updates.items():
        setattr(playlist, field_name, value)

    if payload.song_ids is not None:
        playlist.songs = _resolve_songs(session, payload.song_ids)

    session.commit()
    updated_playlist = get_playlist_by_id(session, playlist.id)
    if updated_playlist is None:
        raise RuntimeError("Updated playlist could not be reloaded")
    logger.info("Updated playlist id=%s with fields=%s.", original_playlist_id, sorted(updates))
    return updated_playlist


def delete_playlist(session: Session, playlist: Playlist) -> None:
    playlist_id = playlist.id
    session.delete(playlist)
    session.commit()
    logger.info("Deleted playlist id=%s.", playlist_id)


def add_song_to_playlist(session: Session, playlist: Playlist, song: Song) -> Playlist:
    if any(existing_song.id == song.id for existing_song in playlist.songs):
        logger.debug(
            "Song id=%s already linked to playlist id=%s. Skipping insert.",
            song.id,
            playlist.id,
        )
        return playlist

    playlist.songs.append(song)
    session.commit()
    updated_playlist = get_playlist_by_id(session, playlist.id)
    if updated_playlist is None:
        raise RuntimeError("Updated playlist could not be reloaded")
    logger.info("Added song id=%s to playlist id=%s.", song.id, playlist.id)
    return updated_playlist


def remove_song_from_playlist(session: Session, playlist: Playlist, song: Song) -> Playlist | None:
    linked_song = next((item for item in playlist.songs if item.id == song.id), None)
    if linked_song is None:
        logger.debug(
            "Song id=%s is not linked to playlist id=%s. Nothing to remove.",
            song.id,
            playlist.id,
        )
        return None

    playlist.songs.remove(linked_song)
    session.commit()
    logger.info("Removed song id=%s from playlist id=%s.", song.id, playlist.id)
    return get_playlist_by_id(session, playlist.id)

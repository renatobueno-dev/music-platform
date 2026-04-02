"""Association-table ORM model definitions."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PlaylistSong(Base):
    """Persisted link between a playlist and a song."""

    __tablename__ = "playlist_songs"

    playlist_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("playlists.id", ondelete="CASCADE"),
        primary_key=True,
    )
    song_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("songs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("(CURRENT_TIMESTAMP)"),
        nullable=False,
    )

    def relation_key(self) -> tuple[int, int]:
        """Return the composite key that identifies this association row."""
        return (self.playlist_id, self.song_id)

    def references_song(self, song_id: int) -> bool:
        """Return whether this association row references the given song id."""
        return self.song_id == song_id

"""Playlist ORM model definitions."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.song import Song


class Playlist(Base):
    """Persisted playlist record with linked songs."""

    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("(CURRENT_TIMESTAMP)"),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("(CURRENT_TIMESTAMP)"),
        onupdate=text("(CURRENT_TIMESTAMP)"),
        nullable=False,
    )

    songs: Mapped[list["Song"]] = relationship(
        secondary="playlist_songs",
    )

    def visibility_label(self) -> str:
        """Return a stable human-readable visibility label."""
        return "public" if self.is_public else "private"

    def song_ids(self) -> list[int]:
        """Return linked song identifiers in their current relationship order."""
        return [song.id for song in self.songs]

"""Song ORM model definitions."""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Song(Base):
    """Persisted song record exposed by the API."""

    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist: Mapped[str] = mapped_column(String(255), nullable=False)
    album: Mapped[str | None] = mapped_column(String(255), nullable=True)
    genre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    release_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    release_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("(CURRENT_TIMESTAMP)"),
        nullable=False,
    )

    def display_title(self) -> str:
        """Return a human-readable title line for logs and debugging."""
        return f"{self.artist} - {self.title}"

    def release_reference(self) -> str | None:
        """Return the most precise available release reference."""
        if self.release_date is not None:
            return self.release_date.isoformat()
        if self.release_year is not None:
            return str(self.release_year)
        return None

"""Pydantic schemas for playlist request and response payloads."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.schemas.song import SongRead


class PlaylistCreate(BaseModel):
    """Payload required to create a playlist."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    is_public: bool = True
    song_ids: list[PositiveInt] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class PlaylistUpdate(BaseModel):
    """Partial payload accepted when updating a playlist."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    is_public: bool | None = None
    song_ids: list[PositiveInt] | None = None

    model_config = ConfigDict(extra="forbid")


class PlaylistRead(BaseModel):
    """Serialized playlist returned by the API."""

    id: int
    name: str
    description: str | None
    is_public: bool
    songs: list[SongRead]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

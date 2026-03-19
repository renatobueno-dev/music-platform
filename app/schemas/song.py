from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class SongCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    artist: str = Field(min_length=1, max_length=255)
    album: str | None = Field(default=None, max_length=255)
    genre: str | None = Field(default=None, max_length=100)
    duration_seconds: int | None = Field(default=None, ge=1)
    release_date: date | None = None
    release_year: int | None = Field(default=None, ge=1800, le=2100)

    model_config = ConfigDict(extra="forbid")


class SongUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    artist: str | None = Field(default=None, min_length=1, max_length=255)
    album: str | None = Field(default=None, max_length=255)
    genre: str | None = Field(default=None, max_length=100)
    duration_seconds: int | None = Field(default=None, ge=1)
    release_date: date | None = None
    release_year: int | None = Field(default=None, ge=1800, le=2100)

    model_config = ConfigDict(extra="forbid")


class SongRead(BaseModel):
    id: int
    title: str
    artist: str
    album: str | None
    genre: str | None
    duration_seconds: int | None
    release_date: date | None
    release_year: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

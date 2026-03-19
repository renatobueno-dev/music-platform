from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PlaylistBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    is_public: bool = True


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistRead(PlaylistBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

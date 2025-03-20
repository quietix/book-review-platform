from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseGenre(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GenrePreview(BaseGenre):
    id: int
    genre: str


class GenreCreate(BaseGenre):
    genre: str


class GenreUpdate(BaseGenre):
    genre: Optional[str]

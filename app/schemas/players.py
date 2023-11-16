# app/schemas/players.py

from typing import List,Optional
from pydantic import BaseModel,validator

class PlayerBase(BaseModel):
    username: str
    rating: int

class PlayersScheme(PlayerBase):
    id: int

    class Config:
        orm_mode = True
class RatingPoint(BaseModel):
    value: int
    date: str

class RatingHistoryEntry(BaseModel):
    name: str
    points: List[RatingPoint]

class PlayerWithRatingHistory(PlayersScheme):
    rating_history: List[RatingHistoryEntry]

    @validator("rating_history", pre=True, each_item=True)
    def validate_rating_history(cls, value):
        required_keys = {'name', 'points'}
        if not all(key in value for key in required_keys):
            raise ValueError(f"Missing required keys in rating history entry. Required: {required_keys}")
        return value

    class Config:
        orm_mode = True

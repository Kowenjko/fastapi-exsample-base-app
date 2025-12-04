from pydantic import BaseModel, ConfigDict
from datetime import datetime

from typing import Literal


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class UserUpdate(UserBase):
    username: str | None = None


class UserStatsRequest(BaseModel):
    user_id: int
    stat_type: Literal["addresses", "spam-and-eggs"]


class UserStatsResponse(BaseModel):
    user_id: int
    stat_type: Literal["addresses", "spam-and-eggs"]
    addresses: int = 0

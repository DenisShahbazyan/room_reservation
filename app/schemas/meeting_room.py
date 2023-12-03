from typing import Optional

from pydantic import BaseModel, Field


class MeetingRoomCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str]

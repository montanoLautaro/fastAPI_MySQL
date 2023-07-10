from pydantic import BaseModel
from typing import Optional


class EntertainmentBase(BaseModel):
    title: str
    type: str
    review: Optional[str]
    image: Optional[str]
    duration: Optional[str]
    score: Optional[str]
    repeat: Optional[bool]
    user_id: str

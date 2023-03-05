from pydantic import BaseModel
from typing import Optional

class BirdIn(BaseModel):
    name: str
    description: Optional[str]
    picture_url: Optional[str]
    family: Optional[str]


class BirdOut(BirdIn):
    id: int

class Error(BaseModel):
    message: str

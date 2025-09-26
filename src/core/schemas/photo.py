from pydantic import BaseModel
from typing import List, Optional

class TagSchema(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True


class PhotoSchema(BaseModel):
    id: int
    url: str
    public_id: str
    description: Optional[str]
    tags: List[TagSchema] = []

    class Config:
        orm_mode = True


from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BlogBase(BaseModel):
    title: str
    content: str
    user: str

class BlogCreate(BaseModel):
    title: str
    content: str

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class BlogResponse(BlogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BlogCreateResponse(BaseModel):
    id: int
    message: str

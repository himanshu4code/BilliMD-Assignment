from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Blog(BaseModel):
    __tablename__ = "blogs"

    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user = Column(String)

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, nullable=False, comment="Unique identifier for the post")
    text = Column(Text, index=False, nullable=False, comment="Text content of the post")
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment="ID of the user who owns the post")

    owner = relationship('User')

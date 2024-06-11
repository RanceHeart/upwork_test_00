from sqlalchemy import Column, Integer, String
from ..database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False, comment="Unique identifier for the user")
    email = Column(String(255), unique=True, index=True, nullable=False, comment="User's email address")
    hashed_password = Column(String(255), nullable=False, comment="Hashed password for the user")

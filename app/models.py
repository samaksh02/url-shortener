from sqlalchemy import Column, String
from .database import Base

class URL(Base):
    __tablename__ = "urls"

    short_code = Column(String, primary_key=True, index=True)
    long_url = Column(String, nullable=False, unique=True)
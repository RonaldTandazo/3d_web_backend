from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
from sqlalchemy.orm import relationship
import datetime

class Software(Base):
    __tablename__ = "softwares"

    software_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), index=True, unique=True, nullable=False)
    image = Column(String(255), default=None, nullable=True)
    status = Column(String(3), default="A", nullable=False)
    ip = Column(String(20), nullable=False)
    terminal = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    artwork_softwares = relationship("ArtworkSoftware", back_populates="software")
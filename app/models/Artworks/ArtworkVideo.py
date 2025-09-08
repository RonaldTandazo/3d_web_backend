from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class ArtworkVideo(Base):
    __tablename__ = "artwork_video"

    artwork_video_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    artwork_id = Column(Integer, ForeignKey("artworks.artwork_id"), nullable=False)
    filename = Column(String(50), nullable=False)
    video_name = Column(String(50), nullable=False)
    status = Column(String(3), default="A", nullable=False)
    ip = Column(String(20), nullable=False)
    terminal = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    artwork = relationship("Artwork")
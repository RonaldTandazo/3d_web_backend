from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class Artwork(Base):
    __tablename__ = "artworks"

    artwork_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), index=True, unique=True)
    description = Column(String(255))
    mature_content = Column(Boolean)
    publishing_id = Column(Integer, ForeignKey("publishing.publishing_id"))
    status = Column(String(3))
    ip = Column(String(20))
    terminal = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    publishing = relationship("Publishing")
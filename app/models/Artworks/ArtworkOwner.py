from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class ArtworkOwner(Base):
    __tablename__ = "artwork_owner"

    artwork_owner_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    artwork_id = Column(Integer, ForeignKey("artworks.artwork_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    status = Column(String(3), default="A")
    ip = Column(String(20))
    terminal = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    artwork = relationship("Artwork")
    user = relationship("User")
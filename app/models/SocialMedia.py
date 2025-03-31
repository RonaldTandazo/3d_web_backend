from sqlalchemy import Column, Integer, String, DateTime
import datetime
from app.models.base import Base

class SocialMedia(Base):
    __tablename__ = "social_media"

    social_media_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), index=True, unique=True)
    status = Column(String(3))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

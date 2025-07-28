from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from app.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

class UserSocialNetwork(Base):
    __tablename__ = "user_social_network"

    user_social_network_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    social_media_id = Column(Integer, ForeignKey("social_media.social_media_id"))
    link = Column(String(255))
    status = Column(String(3), default="A")
    ip = Column(String(20))
    terminal = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    user = relationship("User")
    socialMedia = relationship(
        "SocialMedia",
        primaryjoin="and_(UserSocialNetwork.social_media_id == SocialMedia.social_media_id, SocialMedia.status == 'A')"
    )
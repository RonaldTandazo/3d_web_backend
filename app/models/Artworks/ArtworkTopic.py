from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class ArtworkTopic(Base):
    __tablename__ = "artwork_topics"

    artwork_topic_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    artwork_id = Column(Integer, ForeignKey("artworks.artwork_id"))
    topic_id = Column(Integer, ForeignKey("topics.topic_id"))
    status = Column(String(3), default="A")
    ip = Column(String(20))
    terminal = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    artwork = relationship("Artwork")
    topic = relationship(
        "Topic",
        back_populates="artwork_topics",
        primaryjoin="and_(ArtworkTopic.topic_id == Topic.topic_id, Topic.status == 'A')"
    )
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from app.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

class UserTopic(Base):
    __tablename__ = "user_topics"

    user_topic_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    topic_id = Column(Integer, ForeignKey("topics.topic_id"))
    status = Column(String(3), default="A")
    ip = Column(String(20))
    terminal = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    user = relationship("User")
    topic = relationship("Topic")
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
import datetime
from app.models.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    refresh_token_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
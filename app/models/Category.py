from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
import datetime

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), index=True, unique=True)
    status = Column(String(3))
    ip = Column(String(20))
    terminal = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

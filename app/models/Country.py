from sqlalchemy import Column, Integer, String, DateTime
import datetime
from app.models.base import Base

class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), index=True, unique=True)
    status = Column(String(3))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

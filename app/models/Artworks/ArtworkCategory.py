from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class ArtworkCategory(Base):
    __tablename__ = "artwork_categories"

    artwork_category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    artwork_id = Column(Integer, ForeignKey("artworks.artwork_id"))
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    status = Column(String(3), default="A")
    ip = Column(String(20))
    terminal = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    artwork = relationship("Artwork", back_populates="artwork_categories")
    category = relationship(
        "Category", 
        back_populates="artwork_categories", 
        primaryjoin="and_(ArtworkCategory.category_id == Category.category_id, Category.status == 'A')"
    )
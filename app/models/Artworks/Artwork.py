from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime


class Artwork(Base):
    __tablename__ = "artworks"

    artwork_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), index=True)
    description = Column(String(255))
    mature_content = Column(Boolean)
    publishing_id = Column(Integer, ForeignKey("publishing.publishing_id"))
    has_images = Column(Boolean, nullable=True, default=False)
    has_videos = Column(Boolean, nullable=True, default=False)
    has_3d_file = Column(Boolean, nullable=True, default=False)
    status = Column(String(3), default="A")
    ip = Column(String(20))
    terminal = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    publishing = relationship("Publishing")
    artwork_thumbnail = relationship("ArtworkThumbnail", back_populates="artwork", uselist=False)
    artwork_categories = relationship(
        "ArtworkCategory", 
        back_populates="artwork", 
        primaryjoin="and_(Artwork.artwork_id == ArtworkCategory.artwork_id, ArtworkCategory.status == 'A')",
        uselist=True
    )
    artwork_softwares = relationship(
        "ArtworkSoftware", 
        back_populates="artwork", 
        primaryjoin="and_(Artwork.artwork_id == ArtworkSoftware.artwork_id, ArtworkSoftware.status == 'A')",
        uselist=True
    )
    artwork_topics = relationship(
        "ArtworkTopic", 
        back_populates="artwork", 
        primaryjoin="and_(Artwork.artwork_id == ArtworkTopic.artwork_id, ArtworkTopic.status == 'A')",
        uselist=True
    )
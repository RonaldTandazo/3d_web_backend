from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
import datetime
from app.models.base import Base
from sqlalchemy.dialects.postgresql import JSONB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    professional_headline = Column(String(255), nullable=True)
    summary = Column(String(255), nullable=True)
    city = Column(String(50), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=True)
    avatar = Column(String(50), nullable=True)
    status = Column(String(3), default="A", nullable=False)
    ip = Column(String(20), nullable=False)
    terminal = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)

    country = relationship(
        "Country",
        primaryjoin="and_(User.country_id == Country.country_id, Country.status == 'A')"
    )

    @classmethod
    def verifyPassword(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hashPassword(cls, password):
        return pwd_context.hash(password)

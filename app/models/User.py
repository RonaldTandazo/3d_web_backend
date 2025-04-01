from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
import datetime
from app.models.base import Base
from app.models.Country import Country

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(50))
    professional_headline = Column(String(255))
    city = Column(String(50))
    country_id = Column(Integer, ForeignKey("countries.country_id"))
    status = Column(String(3))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    country = relationship("Country")

    @classmethod
    def verifyPassword(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hashPassword(cls, password):
        return pwd_context.hash(password)

from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext
from app.models.base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(50))
    active = Column(String(50))

    @classmethod
    def verifyPassword(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hashPassword(cls, password):
        return pwd_context.hash(password)

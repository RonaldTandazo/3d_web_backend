from sqlalchemy.ext.asyncio import AsyncSession
from app.models.User import User
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.config.logger import logger
from sqlalchemy import and_
from fastapi import Depends
from app.db.database import get_db

class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def loginUser(self, email, password):
        try:
            result = await self.db.execute(select(User).filter(and_(User.email == email, User.active == "A")))
            user = result.scalars().first()

            if user and User.verifyPassword(password, user.password):
                return user
            return None

        except SQLAlchemyError as e:
            logger.error(f"Database error while logging in: {str(e)}")
            raise Exception("Database error occurred while logging in.")

        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            raise Exception("Unexpected error occurred during login.")

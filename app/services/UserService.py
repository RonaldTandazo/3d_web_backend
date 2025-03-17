from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.User import User
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import and_

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def getUserById(self, user_id: int):
        try:
            result = await self.db.execute(select(User).filter(User.id == user_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching user {user_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching user {user_id}: {str(e)}")
            return None
        
    async def getUserByEmail(self, email: str):
        try:
            result = await self.db.execute(select(User).filter(and_(User.email == email, User.active == "A")))
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching user {email}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching user {email}: {str(e)}")
            return None

    async def registerUser(self, name: str, email: str, password: str):
        try:
            existing_user = await self.getUserByEmail(email)
            if existing_user:
                return None

            hashed_password = User.hashPassword(password)
            user = User(name=name, email=email, password=hashed_password, active="A")
            self.db.add(user)
            await self.db.commit()

            return user
        except IntegrityError as e:
            logger.warning(f"Integrity error while creating user {email}: {str(e)}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating user {email}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while creating user {email}: {str(e)}")
            return None
        
    async def changePassword(self, user: User, new_password: str):
        try:
            user.password = User.hashPassword(new_password)
            await self.db.commit()

            return user
        except SQLAlchemyError as e:
            logger.error(f"Database error while changing password for user {user.email}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while changing password for user {user.email}: {str(e)}")
            return None

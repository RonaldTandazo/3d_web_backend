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
        
    async def getUserByUsename(self, username: str):
        try:
            result = await self.db.execute(select(User).filter(and_(User.username == username, User.active == "A")))
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching user {username}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching user {username}: {str(e)}")
            return None

    async def registerUser(self, firstName: str, lastName: str, username: str, email: str, password: str):
        try:
            if await self.getUserByEmail(email):
                return {"ok": False, "error": "Email already in use", "code": 400}

            if await self.getUserByUsename(username):
                return {"ok": False, "error": "Username already in use", "code": 400}

            hashed_password = User.hashPassword(password)
            user = User(
                first_name=firstName,
                last_name=lastName, 
                username=username, 
                email=email, 
                password=hashed_password, 
                active="A"
            )
            self.db.add(user)
            await self.db.commit()

            return {"ok": True, "message": "User created successfully", "code": 201, "user": user}

        except Exception as e:
            error_mapping = {
                IntegrityError: (400, "Database integrity error"),
                SQLAlchemyError: (500, "Database error"),
                ValueError: (400, "Invalid input data"),
                PermissionError: (401, "Unauthorized access"),
                FileNotFoundError: (404, "Resource not found"),
                ConnectionError: (429, "Too many requests"),
            }

            error_code, error_message = error_mapping.get(type(e), (500, "Internal server error"))
            return {"ok": False, "error": error_message, "code": error_code}
        
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

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Users.User import User
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.config.logger import logger
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def loginUser(self, username, password):
        try:
            result = await self.db.execute(
                select(User)
                .options(joinedload(User.country))
                .filter(and_(User.username == username, User.status == "A"))
            )

            user = result.scalar_one_or_none()
            
            if user :
                if User.verifyPassword(password, user.password):
                    if user.country != None:
                        user.country_name = user.country.name
                    return {"ok": True, "message": "Sign In Success", "code": 201, "data": user}
    
                return {"ok": False, "error": "Invalid Credentials", "code": 400}

            return {"ok": False, "error": "Invalid Credentials", "code": 404}
        except Exception as e:
            logger.error(e)
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

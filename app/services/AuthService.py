from sqlalchemy.ext.asyncio import AsyncSession
from app.models.User import User
from app.models.Country import Country
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.config.logger import logger
from sqlalchemy import and_, join
from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import aliased

class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def loginUser(self, username, password):
        try:
            result = await self.db.execute(
                select(User, Country.name.label("country_name"))
                .join(Country, User.country_id == Country.country_id)
                .filter(and_(User.username == username, User.status == "A"))
            )

            user = result.first()
            if user :
                user, country_name = user
                user.country_name = country_name

                if User.verifyPassword(password, user.password):
                    return {"ok": True, "message": "Sign In Success", "code": 201, "data": user}
    
                return {"ok": False, "error": "Invalid Password", "code": 400}

            return {"ok": False, "error": "User Not Found", "code": 404}
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

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
            result = await self.db.execute(select(User).filter(and_(User.user_id == user_id, User.status == "A")))
            user = result.scalars().first()

            if not user:
                return {"ok": False, "error": "User Not Found", "code": 404}

            return {"ok": True, "message": "User Found", "code": 201, "data": user}
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
        
    async def getUserByEmail(self, email: str):
        try:
            result = await self.db.execute(select(User).filter(and_(User.email == email, User.status == "A")))
            user = result.scalars().first()

            if not user:
                return {"ok": False, "error": "User Not Found", "code": 404}

            return {"ok": True, "message": "User Found", "code": 201, "data": user}
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
        
    async def getUserByUsername(self, username: str):
        try:
            result = await self.db.execute(select(User).filter(and_(User.username == username, User.status == "A")))
            user = result.scalars().first()

            if not user:
                return {"ok": False, "error": "User Not Found", "code": 404}

            return {"ok": True, "message": "User Found", "code": 201, "data": user}
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

    async def registerUser(self, firstName: str, lastName: str, username: str, email: str, password: str):
        try:
            hashed_password = User.hashPassword(password)
            user = User(
                first_name=firstName,
                last_name=lastName, 
                username=username, 
                email=email, 
                password=hashed_password, 
                status="A"
            )
            self.db.add(user)
            await self.db.commit()

            return {"ok": True, "message": "User created successfully", "code": 201, "data": user}

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
        
    async def profileUpdate(self, user: User, firstName: str, lastName: str, professionalHeadline: str, city: str, countryId: int):
        try:
            logger.info(user)
            user.first_name = firstName
            user.last_name = lastName
            user.professional_headline = professionalHeadline 
            user.city = city
            user.country_id = countryId
            await self.db.commit()

            return {"ok": True, "message": "Profile Updated Successfully", "code": 201}
        except Exception as e:
            logger.info(e)
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

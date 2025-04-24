from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.General.Publishing import Publishing
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import asc

class PublishingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def getCategories(self):
        try:
            result = await self.db.execute(select(Publishing).filter(Publishing.status == "A").order_by(asc(Publishing.name)))
            publishing = result.scalars().all()

            if not publishing:
                return {"ok": False, "error": "Publishing Options Not Found", "code": 404}

            return {"ok": True, "message": "Publishing Options Found", "code": 201, "data": publishing}
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
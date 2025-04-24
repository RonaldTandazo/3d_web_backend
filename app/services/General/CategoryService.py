from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.General.Category import Category
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import asc

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def getCategories(self):
        try:
            result = await self.db.execute(select(Category).filter(Category.status == "A").order_by(asc(Category.name)))
            categories = result.scalars().all()

            if not categories:
                return {"ok": False, "error": "Categories Not Found", "code": 404}

            return {"ok": True, "message": "Categories Found", "code": 201, "data": categories}
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
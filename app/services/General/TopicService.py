from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.General.Topic import Topic
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import asc

class TopicService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def getTopics(self):
        try:
            result = await self.db.execute(select(Topic).filter(Topic.status == "A").order_by(asc(Topic.name)))
            topics = result.scalars().all()

            if not topics:
                return {"ok": False, "error": "Topics Not Found", "code": 404}

            return {"ok": True, "message": "Topics Found", "code": 201, "data": topics}
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
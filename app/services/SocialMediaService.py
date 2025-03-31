from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.SocialMedia import SocialMedia
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class SocialMediaService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def getSocialMedia(self):
        try:
            result = await self.db.execute(select(SocialMedia).filter(SocialMedia.status == "A"))
            social_media = result.scalars().all()

            if not social_media:
                return {"ok": False, "error": "Social Media Not Found", "code": 404}

            return {"ok": True, "message": "Social Media Found", "code": 201, "data": social_media}
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
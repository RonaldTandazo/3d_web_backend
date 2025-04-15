from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Artwork import Artwork
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import datetime

class ArtworkService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store(self, title, description, matureContent, ip, terminal, publishing = 3):
        try:
            artwork = Artwork(
                title=title,
                description=description,
                mature_content=matureContent,
                publishing_id=publishing,
                status="A",
                ip=ip,
                terminal=terminal,
                created_at=datetime.datetime.now()
            )
            self.db.add(artwork)
            await self.db.commit()

            return {"ok": True, "message": "Artwork Saved Successfully", "code": 201, "data": artwork}

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
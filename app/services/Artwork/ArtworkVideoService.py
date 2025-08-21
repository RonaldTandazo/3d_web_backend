from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Artworks.ArtworkVideo import ArtworkVideo
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class ArtworkVideoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store(self, artworkId, filename, video_name, ip, terminal):
        try:
            artwork_video = ArtworkVideo(
                artwork_id=artworkId,
                filename=filename,
                video_name=video_name,
                ip=ip,
                terminal=terminal
            )
            self.db.add(artwork_video)
            await self.db.commit()

            return {"ok": True, "message": "Artwork Video Saved Successfully", "code": 201, "data": artwork_video}

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
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Artworks.ArtworkImage import ArtworkImage
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class ArtworkImageService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store(self, artworkId, filename, image_name, ip, terminal):
        try:
            artwork_image = ArtworkImage(
                artwork_id=artworkId,
                filename=filename,
                image_name=image_name,
                ip=ip,
                terminal=terminal
            )
            self.db.add(artwork_image)
            await self.db.commit()

            return {"ok": True, "message": "Artwork Image Saved Successfully", "code": 201, "data": artwork_image}

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
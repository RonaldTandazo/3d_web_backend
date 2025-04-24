from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Artworks.ArtworkCategory import ArtworkCategory
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class ArtworkCategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store(self, artworkId, categoryIds, ip, terminal):
        try:
            artwork_categories = []
            for category_id in categoryIds:
                artwork_category = ArtworkCategory(
                    artwork_id=artworkId,
                    category_id=category_id,
                    ip=ip,
                    terminal=terminal
                )
                artwork_categories.append(artwork_category)
            
            self.db.add_all(artwork_categories)
            await self.db.commit()

            return {"ok": True, "message": "Artwork Categories Saved Successfully", "code": 201, "data": artwork_categories}

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
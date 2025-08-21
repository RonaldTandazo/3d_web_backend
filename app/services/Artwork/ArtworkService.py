from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Artworks.Artwork import Artwork
from app.models.Artworks.ArtworkCategory import ArtworkCategory
from app.models.Artworks.ArtworkSoftware import ArtworkSoftware
from app.models.Artworks.ArtworkTopic import ArtworkTopic
from app.models.Artworks.ArtworkThumbnail import ArtworkThumbnail
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.graphql.Artwork.ArtworkPayloads import StandardPayload
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.orm import selectinload

class ArtworkService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store(self, title, description, matureContent, has_images, has_videos, has_3d_file, ip, terminal, publishing = 3):
        try:
            artwork = Artwork(
                title=title,
                description=description,
                mature_content=matureContent,
                publishing_id=publishing,
                has_images=has_images,
                has_videos=has_videos,
                has_3d_file=has_3d_file,
                ip=ip,
                terminal=terminal
            )
            self.db.add(artwork)
            await self.db.commit()

            return {"ok": True, "message": "Artwork Saved Successfully", "code": 201, "data": artwork}

        except Exception as e:
            logger.error(e)
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
        
    async def getArtworkDetails(self, artworkId):
        try:
            result = await self.db.execute(
                select(Artwork)
                .filter(and_(Artwork.artwork_id == artworkId, Artwork.status == "A"))
                .options(
                    selectinload(Artwork.artwork_categories).selectinload(ArtworkCategory.category), 
                    selectinload(Artwork.artwork_softwares).selectinload(ArtworkSoftware.software),
                    selectinload(Artwork.artwork_topics).selectinload(ArtworkTopic.topic),
                    selectinload(Artwork.artwork_thumbnail).selectinload(ArtworkThumbnail.artwork)
                )
            )
            artwork = result.scalar_one_or_none()

            if not artwork:
                return {"ok": False, "error": "Artwork Details Not Found", "code": 404}
            
            artwork = {
                "artwork_id": artwork.artwork_id,
                "title": artwork.title,
                "description": artwork.description,
                "mature_content": artwork.mature_content,
                "categories": [item.category_id for item in artwork.artwork_categories],
                "topics": [StandardPayload(value=item.topic_id, label=item.topic.name) for item in artwork.artwork_topics],
                "softwares": [StandardPayload(value=item.software_id, label=item.software.name) for item in artwork.artwork_softwares],
                "publishing_id": artwork.publishing_id,
                "thumbnail": artwork.artwork_thumbnail.filename if artwork.artwork_thumbnail else None,
                "created_at": artwork.created_at,
            }

            return {"ok": True, "message": "Artwork Details Found", "code": 201, "data": artwork}
        except Exception as e:
            logger.error(e)
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
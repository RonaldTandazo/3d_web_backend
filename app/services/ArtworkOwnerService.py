from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ArtworkOwner import ArtworkOwner
from app.models.Artwork import Artwork
from app.models.User import User
from app.models.ArtworkThumbnail import ArtworkThumbnail
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import and_, asc
import datetime

class ArtworkOwnerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store(self, artworkId, userId, ip, terminal):
        try:
            artwork_user = ArtworkOwner(
                artwork_id=artworkId,
                user_id=userId,
                status="A",
                ip=ip,
                terminal=terminal,
                created_at=datetime.datetime.now()
            )
            self.db.add(artwork_user)
            await self.db.commit()

            return {"ok": True, "message": "Artwork Owner Saved Successfully", "code": 201, "data": artwork_user}

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
        
    async def getUserArtworks(self, userId):
        try:
            result = await self.db.execute(
                select(
                    Artwork.artwork_id.label("artwork_id"),
                    Artwork.title.label("title"),
                    Artwork.publishing_id.label("publishingId"),
                    Artwork.created_at.label("createdAt"),
                    ArtworkThumbnail.filename.label("thumbnail"),
                    User.username.label("owner")
                )
                .select_from(ArtworkOwner)
                .join(User, and_(ArtworkOwner.user_id == User.user_id))
                .join(Artwork, and_(ArtworkOwner.artwork_id == Artwork.artwork_id, Artwork.status == "A"))
                .outerjoin(ArtworkThumbnail, and_(Artwork.artwork_id == ArtworkThumbnail.artwork_id, ArtworkThumbnail.status == "A"))
                .where(and_(ArtworkOwner.status == "A", ArtworkOwner.user_id == userId))
                .order_by(asc(Artwork.created_at))
            )

            rows = result.mappings().all()

            artworks = [
                {
                    "artwork_id": row.artwork_id,
                    "title": row.title,
                    "thumbnail": row.thumbnail,
                    "publishingId": row.publishingId,
                    "createdAt": row.createdAt,
                    "owner": row.owner,
                }
                for row in rows
            ]

            return {"ok": True, "message": "Artworks Found", "code": 201, "data": artworks}
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
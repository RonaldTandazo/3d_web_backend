from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Artworks.ArtworkTopic import ArtworkTopic
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class ArtworkTopicService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store(self, artworkId, topicIds, ip, terminal):
        try:
            artwork_topics = []
            for topic_id in topicIds:
                artwork_topic = ArtworkTopic(
                    artwork_id=artworkId,
                    topic_id=topic_id,
                    ip=ip,
                    terminal=terminal
                )
                artwork_topics.append(artwork_topic)
            
            self.db.add_all(artwork_topics)
            await self.db.commit()

            return {"ok": True, "message": "Artwork Categories Saved Successfully", "code": 201, "data": artwork_topics}

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
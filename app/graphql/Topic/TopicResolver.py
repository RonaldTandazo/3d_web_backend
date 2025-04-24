import strawberry
from app.services.General.TopicService import TopicService
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.graphql.Topic.TopicPayloads import TopicPayload

@strawberry.type
class TopicQuery:
    @strawberry.field
    async def getTopics(self, info) -> list[TopicPayload]:
        db = info.context["db"]
        topic_Service = TopicService(db)
        try:
            topics = await topic_Service.getTopics()

            if not topics.get("ok", False):
                raise GraphQLError(message=topics['error'], extensions={"code": "BAD_USER_INPUT"})
            
            topics = topics.get("data")

            return [TopicPayload(topicId=topic.topic_id, name=topic.name) for topic in topics]
        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "E-mail already in used"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})
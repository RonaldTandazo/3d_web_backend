import strawberry
from app.services.PublishingService import PublishingService
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.graphql.Publishing.PublishingPayloads import PublishingPayload

@strawberry.type
class PublishingQuery:
    @strawberry.field
    async def getPublishing(self, info) -> list[PublishingPayload]:
        db = info.context["db"]
        publishing_service = PublishingService(db)
        try:
            publishing = await publishing_service.getCategories()

            if not publishing.get("ok", False):
                raise GraphQLError(message=publishing['error'], extensions={"code": "BAD_USER_INPUT"})
            
            publishing = publishing.get("data")

            return [PublishingPayload(publishingId=state.publishing_id, name=state.name) for state in publishing]
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
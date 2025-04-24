import strawberry
from app.services.General.SocialMediaService import SocialMediaService
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.graphql.SocialMedia.SocialMediaPayloads import SocialMediaPayload

@strawberry.type
class SocialMediaQuery:
    @strawberry.field
    async def getSocialMedia(self, info) -> list[SocialMediaPayload]:
        db = info.context["db"]
        social_media_service = SocialMediaService(db)
        try:
            social_media = await social_media_service.getSocialMedia()

            if not social_media.get("ok", False):
                raise GraphQLError(message=social_media['error'], extensions={"code": "BAD_USER_INPUT"})
            
            social_media = social_media.get("data")

            return [SocialMediaPayload(socialMediaId=network.social_media_id, name=network.name) for network in social_media]
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
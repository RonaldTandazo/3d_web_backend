import strawberry
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.graphql.Artwork.ArtworkInputs import StoreArtworkInput
from app.services.ArtworkService import ArtworkService
from app.services.ArtworkOwnerService import ArtworkOwnerService
from app.utils.helpers import Helpers

@strawberry.type
class ArtworkMutation:
    @strawberry.mutation
    async def storeArtwork(self, info, artworkData: StoreArtworkInput) -> str:
        db = info.context["db"]
        current_user = info.context["current_user"]
        request = info.context["request"]
        artwork_service = ArtworkService(db)
        artwork_owner_service = ArtworkOwnerService(db)
        ip = await Helpers.getIp(request)
        terminal = await Helpers.getRequestAgents(request)
        try:
            store_artwork = await artwork_service.store(
                artworkData.title,
                artworkData.description,
                artworkData.matureContent,
                ip,
                terminal,
                artworkData.publishing
            )

            if not store_artwork.get("ok", False):
                raise GraphQLError(message=store_artwork['error'], extensions={"code": "BAD_USER_INPUT"})

            artwork = store_artwork.get("data")

            store_artwork_owner = await artwork_owner_service.store(
                artwork.artwork_id,
                current_user.userId,
                ip,
                terminal
            )

            if not store_artwork_owner.get("ok", False):
                raise GraphQLError(message=store_artwork_owner['error'], extensions={"code": "BAD_USER_INPUT"})
            
            return store_artwork["message"]

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
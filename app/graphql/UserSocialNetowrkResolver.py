import strawberry
from app.services.UserService import UserService
from app.services.UserSocialNetworkService import UserSocialNetworkService 
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.utils.helpers import Helpers

@strawberry.input
class SocialMediaStoreInput:
    socialMediaId: int
    link: str

@strawberry.type
class SocialMediPayload:
    userSocialNetworkId: int
    socialMediaId: int
    network: str
    link: str

@strawberry.type
class UserSocialNetworkQuery:
    @strawberry.field
    async def getUserSocialMedia(self, info) -> list[SocialMediPayload]:
        db = info.context["db"]
        current_user = info.context["current_user"]
        usr_scl_ntw_service = UserSocialNetworkService(db)
        try:
            social_media = await usr_scl_ntw_service.getUserSocialMedia(current_user.userId)

            if not social_media.get("ok", False):
                raise GraphQLError(message=social_media['error'], extensions={"code": "BAD_USER_INPUT"})
            
            social_media = social_media.get("data")

            return [SocialMediPayload(userSocialNetworkId=item['user_social_network_id'], socialMediaId=item['social_media_id'], network=item['network_name'], link=item['link']) for item in social_media]
        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "El correo ya está en uso"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})

@strawberry.type
class UserSocialNetworkMutation:
    @strawberry.mutation
    async def storeUserSocialNetwork(self, info, storeUserNetwork: SocialMediaStoreInput) -> str:
        db = info.context["db"]
        current_user = info.context["current_user"]
        request = info.context["request"]
        user_service = UserService(db)
        usr_scl_ntw_service = UserSocialNetworkService(db)
        ip = await Helpers.getIp(request)
        terminal = await Helpers.getRequestAgents(request)
        try:
            user = await user_service.getUserById(current_user.userId)
            if not user.get("ok", False):
                raise GraphQLError(message=user['error'], extensions={"code": "BAD_USER_INPUT"})

            store = await usr_scl_ntw_service.store(
                current_user.userId,
                storeUserNetwork.socialMediaId, 
                storeUserNetwork.link,
                ip,
                terminal
            )

            if store.get("ok", False):
                return store.get("message")
            
            raise GraphQLError(message=store['error'], extensions={"code": "BAD_USER_INPUT"})

        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "El correo ya está en uso"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})
        
    @strawberry.mutation
    async def removeUserSocialNetwork(self, info, userSocialNetworkId: int) -> str:
        db = info.context["db"]
        current_user = info.context["current_user"]
        user_service = UserService(db)
        usr_scl_ntw_service = UserSocialNetworkService(db)
        try:
            user = await user_service.getUserById(current_user.userId)
            if not user.get("ok", False):
                raise GraphQLError(message=user['error'], extensions={"code": "BAD_USER_INPUT"})

            remove = await usr_scl_ntw_service.remove(
                userSocialNetworkId
            )

            if remove.get("ok", False):
                return remove.get("message")
            
            raise GraphQLError(message=remove['error'], extensions={"code": "BAD_USER_INPUT"})

        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "El correo ya está en uso"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})
        


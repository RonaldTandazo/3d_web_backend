import strawberry
from app.services.Authentication.AuthService import AuthService
from app.config.logger import logger
from strawberry.exceptions import GraphQLError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.graphql.Authentication.AuthPayloads import AuthPayload, ValidateUserPayload
from app.services.Artwork.ArtworkOwnerService import ArtworkOwnerService

@strawberry.type
class AuthQuery:
    @strawberry.field
    async def validateUserAccess(self, info, targetValue: str, module: str) -> ValidateUserPayload:
        db = info.context["db"]
        current_user = info.context["current_user"]
        awk_owner_service = ArtworkOwnerService(db)

        try:
            if module == 'ProfileSettings':
                if current_user.username != targetValue:
                    return ValidateUserPayload(validate=False)  
            elif module == 'ArtWorkEdit':
                validation = await awk_owner_service.validateArtworkOwner(current_user.userId, int(targetValue))
                
                if not validation.get('ok', False):
                    return ValidateUserPayload(validate=False)
                
                if not validation.get('data'):
                    return ValidateUserPayload(validate=False)
                
            return ValidateUserPayload(validate=True)
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

@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def login(self, info, username: str, password: str, rememberMe: bool) -> AuthPayload:
        db = info.context["db"]
        auth_service = AuthService(db)
        try:
            login = await auth_service.loginUser(username, password, rememberMe)
            if login.get("ok", False):
                loginData = login.get("data")
                accessToken = loginData['accessToken']
                refreshToken = loginData['refreshToken']
                
                return AuthPayload(accessToken=accessToken, refreshToken=refreshToken, tokenType="bearer")

            raise GraphQLError(message=login['error'], extensions={"code": "BAD_USER_INPUT"})

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
        
    @strawberry.mutation
    async def refreshToken(self, info, refreshToken: str) -> AuthPayload:
        db = info.context["db"]
        auth_service = AuthService(db)
        try:
            tokens = await auth_service.refreshTokens(refreshToken)
            if tokens.get("ok", False):
                tokensData = tokens.get("data")
                accessToken = tokensData['accessToken']
                refreshToken = tokensData['refreshToken']

                return AuthPayload(accessToken=accessToken, refreshToken=refreshToken, tokenType="bearer")
            raise GraphQLError(message="Token refresh failed", extensions={"code": "UNAUTHENTICATED"})
        except GraphQLError as e:
            logger.error(e.message)
            raise e
        except Exception as e:
            logger.error(e)
            raise GraphQLError(message="Could not refresh token", extensions={"code": "INTERNAL_SERVER_ERROR"})
        
    @strawberry.mutation
    async def revokeToken(self, info, refreshToken: str) -> str:
        db = info.context["db"]
        auth_service = AuthService(db)
        try:
            revoke = await auth_service.revokeToken(refreshToken)
            if not revoke.get("ok", False):
                raise GraphQLError(message="Token refresh failed", extensions={"code": "UNAUTHENTICATED"})

            return revoke.get("message")
        except GraphQLError as e:
            logger.error(e.message)
            raise e
        except Exception as e:
            logger.error(e)
            raise GraphQLError(message="Could not refresh token", extensions={"code": "INTERNAL_SERVER_ERROR"})
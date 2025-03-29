import strawberry
from app.services.AuthService import AuthService
from app.config.logger import logger
from app.security.AuthGraph import createAccessToken
from strawberry.exceptions import GraphQLError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

@strawberry.type
class AuthPayload:
    accessToken: str
    tokenType: str

@strawberry.type
class AuthQuery:
    @strawberry.field
    async def test(self, info) -> str:
        return "sss"

@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def login(self, info, username: str, password: str) -> AuthPayload:
        db = info.context["db"]
        auth_service = AuthService(db)
        try:
            user = await auth_service.loginUser(username, password)

            if user.get("ok", False):
                data = user.get("user")
                token = createAccessToken(data={"sub": data.username, "id_user": data.id, "firstName": data.first_name, "lastName": data.last_name, "email": data.email, "username": data.username})
                return AuthPayload(accessToken=token, tokenType="bearer")

            raise GraphQLError(message=user['error'], extensions={"code": "BAD_USER_INPUT"})

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
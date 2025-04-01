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
                user_data = user.get("data")

                token = createAccessToken(data={
                    "sub": user_data.username,
                    "userId": user_data.user_id,
                    "firstName": user_data.first_name, 
                    "lastName": user_data.last_name, 
                    "email": user_data.email, 
                    "username": user_data.username, 
                    "professionalHeadline": user_data.professional_headline, 
                    "city": user_data.city, 
                    "countryId": user_data.country_id, 
                    "location": user_data.city+", "+user_data.country_name,
                    "since": user_data.created_at.isoformat()
                })
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
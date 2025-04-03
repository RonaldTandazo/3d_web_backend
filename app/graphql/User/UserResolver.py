import strawberry
from app.services.UserService import UserService
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.graphql.User.UserInputs import ProfileInput, RegisterInput

@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def registerUser(self, info, user_data: RegisterInput) -> str:
        db = info.context["db"]
        user_service = UserService(db)
        try:
            email_in_use = await user_service.getUserByEmail(user_data.email)
            if email_in_use.get("ok", True):
                raise GraphQLError(message="Email already in use", extensions={"code": "BAD_USER_INPUT"})
            
            username_in_use = await user_service.getUserByUsername(user_data.username)
            if username_in_use.get("ok", True):
                raise GraphQLError(message="Username already in use", extensions={"code": "BAD_USER_INPUT"})

            user = await user_service.registerUser(
                user_data.firstName, 
                user_data.lastName, 
                user_data.username, 
                user_data.email, 
                user_data.password
            )

            if user.get("ok", False):
                return "User Created Successfully"
            
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

    @strawberry.mutation
    async def profileUpdate(self, info, profile_update: ProfileInput) -> str:
        db = info.context["db"]
        current_user = info.context["current_user"]
        user_service = UserService(db)
        try:
            user = await user_service.getUserById(current_user.userId)
            if not user.get("ok", False):
                raise GraphQLError(message=user['error'], extensions={"code": "BAD_USER_INPUT"})

            user=user.get("data")
            update = await user_service.profileUpdate(
                user,
                profile_update.firstName, 
                profile_update.lastName, 
                profile_update.professionalHeadline, 
                profile_update.city, 
                profile_update.countryId
            )

            if update.get("ok", False):
                return update.get("message")
            
            raise GraphQLError(message=update['error'], extensions={"code": "BAD_USER_INPUT"})

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
    async def changePassword(self, info, currentPassword: str, newPassword: str) -> str:
        db = info.context["db"]
        user_service = UserService(db)
        current_user = info.context["current_user"]
        try:
            user = await user_service.getUserById(current_user.userId)
            if not user.get("ok", False):
                raise GraphQLError(message=user['error'], extensions={"code": "BAD_USER_INPUT"})

            user=user.get("data")
            if not user.verifyPassword(currentPassword, user.password):
                raise GraphQLError(message="Invalid Password", extensions={"code": "BAD_USER_INPUT"})
            
            update = await user_service.changePassword(user, newPassword)
            if not update:
                raise GraphQLError(message=user['error'], extensions={"code": "BAD_USER_INPUT"})
            
            return "Password changed successfully"
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

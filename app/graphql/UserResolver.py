import strawberry
from app.services.UserService import UserService
from fastapi import HTTPException, status
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError

@strawberry.type
class UserType:
    id: int
    email: str
    username: str

@strawberry.input
class UserInput:
    firstName: str
    lastName: str
    username: str
    email: str
    password: str

@strawberry.type
class UserQuery:
    @strawberry.field
    async def getUserProfile(self, info) -> UserType:
        current_user = info.context["current_user"]
        db = info.context["db"]
        user_service = UserService(db)

        user = await user_service.getUserByEmail(current_user.email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")    
        return user

@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def registerUser(self, info, user_data: UserInput) -> str:
        db = info.context["db"]
        user_service = UserService(db)
        try:
            user = await user_service.registerUser(
                user_data.firstName, 
                user_data.lastName, 
                user_data.username, 
                user_data.email, 
                user_data.password
            )

            if user.get("ok", False):
                return "Usuario creado con éxito"
            
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
    async def resetPassword(self, info, email: str) -> str:
        db = info.context["db"]
        user_service = UserService(db)
        
        return await "ssss"

    @strawberry.mutation
    async def changePassword(self, info, current_password: str, new_password: str) -> str:
        db = info.context["db"]
        user_service = UserService(db)
        current_user = info.context["current_user"]
        try:
            user = await user_service.getUserByEmail(current_user.email)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            if not user.verifyPassword(current_password, user.password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
            
            update = await user_service.changePassword(user, new_password)
            
            if not update:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error")
            
            return "Password changed successfully"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error")

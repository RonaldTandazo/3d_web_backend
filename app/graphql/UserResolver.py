import strawberry
from app.services.UserService import UserService
from fastapi import HTTPException, status
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError

@strawberry.type
class UserType:
    id: int
    email: str
    name: str

@strawberry.input
class UserInput:
    name: str
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
            user = await user_service.registerUser(user_data.name, user_data.email, user_data.password)
            if not user:
                raise HTTPException(status_code=400, detail="Email already in use")

            return "User created successfully"

        except IntegrityError:
            logger.warning(f"User with email {user_data.email} already exists.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

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

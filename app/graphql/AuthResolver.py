import strawberry
from app.services.AuthService import AuthService
from app.config.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from app.security.AuthGraph import createAccessToken

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
    async def login(self, info, email: str, password: str) -> AuthPayload:
        db = info.context["db"]
        auth_service = AuthService(db)
        try:
            user = await auth_service.loginUser(email, password)

            if not user:
                return AuthPayload(accessToken="", tokenType="Invalid credentials")
            
            token = createAccessToken(data={"sub": user.email, "id_user": user.id})
            return AuthPayload(accessToken=token, tokenType="bearer")

        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")
            return AuthPayload(accessToken="", tokenType="Database error")

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return AuthPayload(accessToken="", tokenType="Internal Server Error")
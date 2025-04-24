from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.services.User.UserService import UserService
from app.db.database import get_db
from app.config.logger import logger
from app.schemas.TokenData import TokenData

UserRoutes = APIRouter()

def user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)

@UserRoutes.get("/user/{user_id}")
async def get_user(user_id: int, user_service: UserService = Depends(user_service)):
    try:
        user = await user_service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        
        return {"ok": True, "data": user} 
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching user {user_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

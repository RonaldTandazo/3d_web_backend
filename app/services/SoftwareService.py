from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Software import Software
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import asc

class SoftwareService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def getSoftware(self):
        try:
            result = await self.db.execute(select(Software).filter(Software.status == "A").order_by(asc(Software.name)))
            software = result.scalars().all()

            if not software:
                return {"ok": False, "error": "Software Not Found", "code": 404}

            return {"ok": True, "message": "Software Found", "code": 201, "data": software}
        except Exception as e:
            error_mapping = {
                IntegrityError: (400, "Database integrity error"),
                SQLAlchemyError: (500, "Database error"),
                ValueError: (400, "Invalid input data"),
                PermissionError: (401, "Unauthorized access"),
                FileNotFoundError: (404, "Resource not found"),
                ConnectionError: (429, "Too many requests"),
            }

            error_code, error_message = error_mapping.get(type(e), (500, "Internal server error"))
            return {"ok": False, "error": error_message, "code": error_code}
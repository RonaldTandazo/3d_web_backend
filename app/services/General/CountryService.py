from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.General.Country import Country
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import asc

class CountryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def getCountries(self):
        try:
            result = await self.db.execute(select(Country).filter(Country.status == "A").order_by(asc(Country.name)))
            countries = result.scalars().all()

            if not countries:
                return {"ok": False, "error": "Countries Not Found", "code": 404}

            return {"ok": True, "message": "Countries Found", "code": 201, "data": countries}
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
import strawberry
from app.services.CountryService import CountryService
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError

@strawberry.type
class CountryPayload:
    countryId: int
    name: str

@strawberry.type
class CountryQuery:
    @strawberry.field
    async def getCountries(self, info) -> list[CountryPayload]:
        db = info.context["db"]
        country_Service = CountryService(db)
        try:
            countries = await country_Service.getCountries()

            if not countries.get("ok", False):
                raise GraphQLError(message=countries['error'], extensions={"code": "BAD_USER_INPUT"})
            
            countries = countries.get("data")

            return [CountryPayload(countryId=country.country_id, name=country.name) for country in countries]
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
import strawberry
from app.services.General.SoftwareService import SoftwareService
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.graphql.Software.SoftwarePayloads import SoftwarePayload

@strawberry.type
class SoftwareQuery:
    @strawberry.field
    async def getSoftware(self, info) -> list[SoftwarePayload]:
        db = info.context["db"]
        software_service = SoftwareService(db)
        try:
            software = await software_service.getSoftware()

            if not software.get("ok", False):
                raise GraphQLError(message=software['error'], extensions={"code": "BAD_USER_INPUT"})
            
            software = software.get("data")

            return [SoftwarePayload(softwareId=item.software_id, name=item.name) for item in software]
        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "E-mail already in used"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})
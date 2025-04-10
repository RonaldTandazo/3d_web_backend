import strawberry
from app.services.CategoryService import CategoryService
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.graphql.Category.CategoryPayloads import CategoryPayload

@strawberry.type
class CategoryQuery:
    @strawberry.field
    async def getCategories(self, info) -> list[CategoryPayload]:
        db = info.context["db"]
        category_Service = CategoryService(db)
        try:
            categories = await category_Service.getCategories()

            if not categories.get("ok", False):
                raise GraphQLError(message=categories['error'], extensions={"code": "BAD_USER_INPUT"})
            
            categories = categories.get("data")

            return [CategoryPayload(categoryId=category.category_id, name=category.name) for category in categories]
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
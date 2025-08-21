import strawberry
from fastapi import Request
from strawberry.extensions import SchemaExtension
from strawberry.exceptions import GraphQLError
from app.security.AuthGraph import getCurrentUserFromToken
from app.config.logger import logger

class AuthExtension(SchemaExtension):
    def on_request_start(self) -> None:
        info = self.execution_context

        # Obtén el request del contexto. En este caso, ya está en el info.context.get("request")
        request: Request = info.context["request"]

        if request.scope['type'] == 'websocket':
            return
        
        # # Obtener el nombre de la operación para las operaciones libres
        body = info.context["body"]
        operation_name = body.get("operationName")
        
        if operation_name and operation_name in ["RegisterUser", "Login", "RefreshToken", "RevokeToken", "GetArtVerseArtworks"]:
            return

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise GraphQLError(
                message="Authentication is Required",
                extensions={"code": "FORBIDDEN"}
            )
        
        try:
            token = authorization.split("Bearer ")[-1]
            current_user = getCurrentUserFromToken(token)

            if not current_user['ok']:
                raise GraphQLError(
                    message="Token has expired",
                    extensions={"code": "UNAUTHENTICATED"}
                )
            
            # Si es válido, puedes añadir el usuario al contexto
            # Strawberry permite modificar el contexto
            info.context["current_user"] = current_user['data']

        except GraphQLError as e:
            # Re-lanza la excepción para que strawberry la maneje
            raise e
        except Exception:
            raise GraphQLError(
                message="Token is invalid",
                extensions={"code": "UNAUTHENTICATED"}
            )
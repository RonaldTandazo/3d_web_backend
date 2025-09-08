from fastapi import HTTPException, FastAPI, Depends, Header, Request
from strawberry.fastapi import GraphQLRouter
from app.graphql.GraphSchema import GraphSchema 
from app.db.database import get_db
from app.security.AuthGraph import getCurrentUserFromToken
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from strawberry.exceptions import GraphQLError
from fastapi.staticfiles import StaticFiles
from app.config.logger import logger
import json

app = FastAPI()

app.mount("/thumbnails", StaticFiles(directory="app/public/artworks/thumbnails"), name="thumbnails")
app.mount("/avatars", StaticFiles(directory="app/public/users/avatars"), name="avatars")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://artnova.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# GRAPHQL
async def get_context(
    request: Request,
    # authorization: str = Header(None),
    # current_user: None = None,
    db: AsyncSession = Depends(get_db)
):
    body = None
    # operation_name = None

    if request.method == "POST":
        try:
            body = await request.json()
            # operation_name = body.get("operationName")  
        except json.JSONDecodeError:
            pass

        return {"db": db, "request": request, "body": body}
    # logger.info(operation_name)
    # if operation_name and operation_name in FREE_OPERATIONS:
    #     return {"current_user": None, "db": db, "request": request, "body": body}
    
    # if authorization:
    #     token = authorization.split("Bearer ")[-1]
    #     try:
    #         current_user = getCurrentUserFromToken(token)
    #         if current_user['ok']:
    #             return {"current_user": current_user['data'], "db": db, "request": request, "body": body}
            
    #         raise GraphQLError(message="Token has expired", extensions={"code": "UNAUTHENTICATED"})
    #     except GraphQLError as e:
    #         raise GraphQLError(message="Token has expired", extensions={"code": "UNAUTHENTICATED"})
    #     except Exception as e:
    #         raise GraphQLError(message="Token has expired", extensions={"code": "UNAUTHENTICATED"})
    # else:
    #     logger.info("cae aca")
    #     raise GraphQLError(message="Authentication is Required", extensions={"code": "FORBIDDEN"})


graphql_app = GraphQLRouter(schema=GraphSchema, context_getter=get_context, subscription_protocols=[GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL])
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

graphql_ws_router = GraphQLRouter(schema=GraphSchema, subscription_protocols=[GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL])
app.include_router(graphql_ws_router, prefix="/graphql/ws", tags=["graphql_ws"])

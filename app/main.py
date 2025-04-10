from fastapi import FastAPI, Depends, Header, Request
from strawberry.fastapi import GraphQLRouter
from app.graphql.GraphSchema import GraphSchema 
from app.db.database import get_db
from app.security.AuthGraph import getCurrentUserFromToken
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from strawberry.exceptions import GraphQLError
from app.config.logger import logger
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:81"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

FREE_OPERATIONS = ["Login", "RegisterUser"]

# GRAPHQL
async def get_context(
    request: Request,
    authorization: str = Header(None),
    current_user: None = None,
    db: AsyncSession = Depends(get_db)
):
    body = None
    operation_name = None


    if request.method == "POST":
        try:
            body = await request.json()
            operation_name = body.get("operationName")  
        except json.JSONDecodeError:
            pass
    
    if operation_name and operation_name in FREE_OPERATIONS:
        return {"current_user": None, "db": db, "request": request, "body": body}
    
    if authorization:
        token = authorization.split("Bearer ")[-1]
        current_user = getCurrentUserFromToken(token)
    else:
        return GraphQLError(message="Authentication is Required", extensions={"code": "FORBIDDEN"})

    return {"current_user": current_user, "db": db, "request": request, "body": body}

graphql_app = GraphQLRouter(GraphSchema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

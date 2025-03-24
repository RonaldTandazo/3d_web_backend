from fastapi import FastAPI, Depends, Header
from strawberry.fastapi import GraphQLRouter
from app.graphql.GraphSchema import GraphSchema 
from app.db.database import get_db
from app.security.AuthGraph import getCurrentUserFromToken
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware 
from app.config.logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:81"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# GRAPHQL
async def get_context(
    authorization: str = Header(None),
    current_user: None = None,
    db: AsyncSession = Depends(get_db)
):
    if authorization:
        token = authorization.split("Bearer ")[-1]
        current_user = getCurrentUserFromToken(token)
    return {"current_user": current_user, "db": db}


graphql_app = GraphQLRouter(GraphSchema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

import strawberry
from app.graphql.UserResolver import UserQuery, UserMutation
from app.graphql.AuthResolver import AuthQuery, AuthMutation

@strawberry.type
class Query(AuthQuery, UserQuery):
    pass

@strawberry.type
class Mutation(AuthMutation, UserMutation):
    pass

GraphSchema = strawberry.Schema(query=Query, mutation=Mutation)

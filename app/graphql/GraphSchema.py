import strawberry
from app.graphql.UserResolver import UserQuery, UserMutation
from app.graphql.AuthResolver import AuthQuery, AuthMutation
from app.graphql.CountryResolver import CountryQuery
from app.graphql.SocialMediaResolver import SocialMediaQuery
from app.graphql.UserSocialNetowrkResolver import UserSocialNetworkQuery, UserSocialNetworkMutation 

@strawberry.type
class Query(AuthQuery, UserQuery, CountryQuery, SocialMediaQuery, UserSocialNetworkQuery):
    pass

@strawberry.type
class Mutation(AuthMutation, UserMutation, UserSocialNetworkMutation):
    pass

GraphSchema = strawberry.Schema(query=Query, mutation=Mutation)

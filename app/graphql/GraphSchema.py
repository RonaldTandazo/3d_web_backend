import strawberry
from app.graphql.User.UserResolver import UserMutation
from app.graphql.Authentication.AuthResolver import AuthQuery, AuthMutation
from app.graphql.Country.CountryResolver import CountryQuery
from app.graphql.SocialMedia.SocialMediaResolver import SocialMediaQuery
from app.graphql.UserSocialNetwork.UserSocialNetowrkResolver import UserSocialNetworkQuery, UserSocialNetworkMutation
from app.graphql.Category.CategoryResolver import  CategoryQuery
from app.graphql.Publishing.PublishingResolver import PublishingQuery
from app.graphql.Software.SoftwareResolver import SoftwareQuery
from app.graphql.Artwork.ArtworkResolver import ArtworkMutation, ArtworkQuery

@strawberry.type
class Query(AuthQuery, CountryQuery, SocialMediaQuery, UserSocialNetworkQuery, CategoryQuery, PublishingQuery, SoftwareQuery, ArtworkQuery):
    pass

@strawberry.type
class Mutation(AuthMutation, UserMutation, UserSocialNetworkMutation, ArtworkMutation):
    pass

GraphSchema = strawberry.Schema(query=Query, mutation=Mutation)

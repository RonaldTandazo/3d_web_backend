import strawberry
from app.graphql import AuthExtension
from app.graphql.User.UserResolver import UserMutation
from app.graphql.Authentication.AuthResolver import AuthQuery, AuthMutation
from app.graphql.Country.CountryResolver import CountryQuery
from app.graphql.SocialMedia.SocialMediaResolver import SocialMediaQuery
from app.graphql.UserSocialNetwork.UserSocialNetowrkResolver import UserSocialNetworkQuery, UserSocialNetworkMutation
from app.graphql.Category.CategoryResolver import  CategoryQuery
from app.graphql.Publishing.PublishingResolver import PublishingQuery
from app.graphql.Software.SoftwareResolver import SoftwareQuery
from app.graphql.Artwork.ArtworkResolver import ArtworkMutation, ArtworkQuery, ArtworkSubscription
from app.graphql.Topic.TopicResolver import TopicQuery
from app.graphql.UserSkills.UserSkillsResolver import UserSkillsQuery, UserSkillsMutation

@strawberry.type
class Query(AuthQuery, CountryQuery, UserSkillsQuery, SocialMediaQuery, UserSocialNetworkQuery, CategoryQuery, PublishingQuery, SoftwareQuery, TopicQuery, ArtworkQuery):
    pass

@strawberry.type
class Mutation(AuthMutation, UserMutation, UserSkillsMutation, UserSocialNetworkMutation, ArtworkMutation):
    pass

@strawberry.type
class Subscription(ArtworkSubscription):
    pass

GraphSchema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription, extensions=[AuthExtension.AuthExtension()])

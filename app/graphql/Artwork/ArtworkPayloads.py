from app.graphql.Category.CategoryPayloads import CategoryPayload
from app.graphql.Topic.TopicPayloads import TopicPayload
from app.graphql.Software.SoftwarePayloads import SoftwarePayload
from app.graphql.Publishing.PublishingPayloads import PublishingPayload
from app.graphql.Standard.StandardPayloads import StandardPayload
import strawberry

@strawberry.type
class ArtworkPayload:
    artworkId: int
    title: str
    thumbnail: str | None
    publishingId: int
    owner: str
    avatar: str | None
    createdAt: str

@strawberry.type
class ArtworkDetailsPayload:
    artworkId: int
    title: str
    description: str
    matureContent: bool
    categories: list[int]
    topics: list[StandardPayload]
    softwares: list[StandardPayload]
    publishingId: int
    thumbnail: str | None
    createdAt: str

@strawberry.type
class ArtworkFormData:
    categories: list[CategoryPayload]
    topics: list[TopicPayload]
    softwares: list[SoftwarePayload]
    publishing: list[PublishingPayload]
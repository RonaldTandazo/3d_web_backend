from app.graphql.Category.CategoryPayloads import CategoryPayload
from app.graphql.Topic.TopicPayloads import TopicPayload
from app.graphql.Software.SoftwarePayloads import SoftwarePayload
from app.graphql.Publishing.PublishingPayloads import PublishingPayload
from app.graphql.Standard.StandardPayloads import StandardPayload
from typing import Optional
import strawberry

@strawberry.type
class ArtworkPayload:
    artworkId: int
    title: str
    thumbnail: Optional[str | None] = None
    publishingId: int
    hasImages: bool = False
    hasVideos: bool = False
    has3DFile: bool = False
    owner: str
    avatar: Optional[str | None] = None
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
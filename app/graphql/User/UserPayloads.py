from app.graphql.Category.CategoryPayloads import CategoryPayload
from app.graphql.Topic.TopicPayloads import TopicPayload
from app.graphql.Software.SoftwarePayloads import SoftwarePayload
from app.graphql.Publishing.PublishingPayloads import PublishingPayload
import strawberry

@strawberry.type
class SkillsData:
    categories: list[CategoryPayload]
    topics: list[TopicPayload]
    softwares: list[SoftwarePayload]
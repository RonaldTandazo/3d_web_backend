
import strawberry

@strawberry.type
class TopicPayload:
    topicId: int
    name: str
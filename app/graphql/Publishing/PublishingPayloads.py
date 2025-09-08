
import strawberry

@strawberry.type
class PublishingPayload:
    publishingId: int
    name: str
    type: str | None
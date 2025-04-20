import strawberry

@strawberry.type
class ArtworkPayload:
    artworkId: int
    title: str
    thumbnail: str
    publishingId: int
    owner: str
    createdAt: str
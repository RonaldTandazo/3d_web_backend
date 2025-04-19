import strawberry

@strawberry.type
class ArtworkPayload:
    artworkId: int
    title: str
    thumbnail: str
    owner: str
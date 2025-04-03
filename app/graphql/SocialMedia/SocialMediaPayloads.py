import strawberry

@strawberry.type
class SocialMediaPayload:
    socialMediaId: int
    name: str
import strawberry

@strawberry.type
class SocialMediPayload:
    userSocialNetworkId: int
    socialMediaId: int
    network: str
    link: str
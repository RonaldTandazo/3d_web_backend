import strawberry

@strawberry.input
class SocialMediaStoreInput:
    socialMediaId: int
    link: str

@strawberry.input
class UpdateUserNetworkInput:
    userSocialNetworkId: int
    socialMediaId: int
    link: str
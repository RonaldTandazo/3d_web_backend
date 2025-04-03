import strawberry

@strawberry.type
class AuthPayload:
    accessToken: str
    tokenType: str
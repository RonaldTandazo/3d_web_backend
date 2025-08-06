import strawberry

@strawberry.type
class AuthPayload:
    accessToken: str
    refreshToken: str
    tokenType: str

@strawberry.type
class ValidateUserPayload:
    validate: bool
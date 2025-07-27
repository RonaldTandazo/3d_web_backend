import strawberry

@strawberry.type
class AuthPayload:
    accessToken: str
    tokenType: str

@strawberry.type
class ValidateUserPayload:
    validate: bool
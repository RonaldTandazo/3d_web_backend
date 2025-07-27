import strawberry

@strawberry.input
class RegisterInput:
    firstName: str
    lastName: str
    username: str
    email: str
    password: str

@strawberry.input
class ProfileInput:
    firstName: str
    lastName: str
    professionalHeadline: str
    summary: str
    countryId: int
    city: str
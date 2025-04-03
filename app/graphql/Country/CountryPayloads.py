
import strawberry

@strawberry.type
class CountryPayload:
    countryId: int
    name: str
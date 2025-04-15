
import strawberry

@strawberry.type
class SoftwarePayload:
    softwareId: int
    name: str
import strawberry

@strawberry.type
class StandardPayload:
    value: int
    label: str

@strawberry.type
class ResponsesPayload:
    value: str
    label: str
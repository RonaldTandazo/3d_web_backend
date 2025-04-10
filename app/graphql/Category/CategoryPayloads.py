
import strawberry

@strawberry.type
class CategoryPayload:
    categoryId: int
    name: str
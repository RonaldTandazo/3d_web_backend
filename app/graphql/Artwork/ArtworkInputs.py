import strawberry
from typing import Optional

@strawberry.input
class StoreArtworkInput:
    title: Optional[str] = None
    description: Optional[str] = None
    matureContent: Optional[bool] = None
    categories: Optional[list[int]] = None
    softwares: Optional[list[int]] = None
    thumbnail: Optional[str] = None
    publishing: Optional[int] = None
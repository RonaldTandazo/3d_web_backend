import strawberry
from typing import Optional

@strawberry.input
class StoreArtworkInput:
    title: Optional[str] = None
    description: Optional[str] = None
    matureContent: Optional[bool] = None
    categories: Optional[list[int]] = None
    topics: Optional[list[int]] = None
    softwares: Optional[list[int]] = None
    images: Optional[list[str]] = None,
    videos: Optional[list[str]] = None,
    file3d: Optional[str] = None,
    thumbnail: Optional[str] = None
    publishing: Optional[int] = None
    schedule: Optional[bool] = None
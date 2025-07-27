import strawberry
from typing import Optional

@strawberry.input
class UserSkillsInput:
    categories: Optional[list[int]] = None
    topics: Optional[list[int]] = None
    softwares: Optional[list[int]] = None
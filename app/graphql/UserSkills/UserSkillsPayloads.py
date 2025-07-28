import strawberry

@strawberry.type
class UserSoftwarePayload:
    userId: int
    softwareId: int
    software: str

@strawberry.type
class UserCategoryPayload:
    userId: int
    categoryId: int
    category: str

@strawberry.type
class UserTopicPayload:
    userId: int
    topicId: int
    topic: str

@strawberry.type
class UserSkillsPayload:
    userTopics: list[UserTopicPayload]
    userSoftwares: list[UserSoftwarePayload]
    userCategories: list[UserCategoryPayload]
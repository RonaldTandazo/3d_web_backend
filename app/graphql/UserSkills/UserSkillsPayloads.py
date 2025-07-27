import strawberry

@strawberry.type
class UserSoftwarePayload:
    userId: int
    softwareId: int

@strawberry.type
class UserCategoryPayload:
    userId: int
    categoryId: int

@strawberry.type
class UserTopicPayload:
    userId: int
    topicId: int

@strawberry.type
class UserSkillsPayload:
    userTopics: list[UserTopicPayload]
    userSoftwares: list[UserSoftwarePayload]
    userCategories: list[UserCategoryPayload]
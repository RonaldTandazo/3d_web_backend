from pydantic import BaseModel

class TokenData(BaseModel):
    email: str
    id_user: int

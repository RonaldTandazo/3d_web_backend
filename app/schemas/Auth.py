from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True 

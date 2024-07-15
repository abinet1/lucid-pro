from pydantic import BaseModel, Field, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Token):
    id: int | None = None
    email: EmailStr | None = None

class User(BaseModel):
    id: int
    email: EmailStr | None = None

class UserBase(BaseModel):
    email: EmailStr
    password: str

class Post(BaseModel):
    post: str = Field(..., min_length=10, max_length=250)
    
class PostBase(Post):
    id: int
    date: str
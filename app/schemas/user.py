from pydantic import BaseModel, EmailStr
from app.db.models import UserRole


class UserLogin(BaseModel):
    """Schema para login de usuário."""
    username: str
    password: str


class Token(BaseModel):
    """Schema para resposta com token JWT."""
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    """Schema para criação de usuário."""
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    """Schema de resposta ao registrar um usuário."""
    id: int
    username: str
    email: str
    role: UserRole

    class Config:
        orm_mode = True

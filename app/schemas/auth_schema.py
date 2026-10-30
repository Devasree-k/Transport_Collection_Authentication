from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field
Role = Literal["admin", "driver"]

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: Role
    is_active: bool

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=20)

class LogoutResponse(BaseModel):
    message: str

class TokenInfoResponse(BaseModel):
    user_id: int
    role: Role
    token_type: str

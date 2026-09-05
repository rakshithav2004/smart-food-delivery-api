from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"
    DELIVERY_PARTNER = "DELIVERY_PARTNER"
    ADMIN = "ADMIN"

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RoleUpdate(BaseModel):
    role: UserRole
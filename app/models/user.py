from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"
    DELIVERY_PARTNER = "DELIVERY_PARTNER"
    ADMIN = "ADMIN"

class User(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
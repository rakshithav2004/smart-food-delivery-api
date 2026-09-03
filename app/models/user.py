from datetime import datetime, timezone

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    email: str
    password: str
    role: str = "CUSTOMER"
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
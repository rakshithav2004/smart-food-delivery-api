from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    name: str
    description: str | None = None
    address: str
    cuisine: str
    owner_id: str
    is_active: bool = True
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
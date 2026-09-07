from datetime import datetime, timezone

from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    restaurant_id: str
    name: str
    description: str | None = None
    price: float
    category: str
    is_available: bool = True
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
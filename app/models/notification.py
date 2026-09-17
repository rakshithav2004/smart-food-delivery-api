from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Notification(BaseModel):
    user_id: str
    type: str
    message: str
    order_id: str | None = None
    is_read: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
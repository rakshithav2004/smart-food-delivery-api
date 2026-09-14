from datetime import datetime, timezone
from pydantic import BaseModel, Field


class DeliveryPartner(BaseModel):
    user_id: str
    phone: str
    vehicle_type: str
    vehicle_number: str
    is_available: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
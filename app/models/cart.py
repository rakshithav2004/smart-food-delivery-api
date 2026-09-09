from datetime import datetime, timezone

from pydantic import BaseModel, Field


class CartItem(BaseModel):
    menu_id: str
    name: str
    price: float
    quantity: int
    subtotal: float


class Cart(BaseModel):
    user_id: str
    items: list[CartItem] = []
    total_amount: float = 0.0
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
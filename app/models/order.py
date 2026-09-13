from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY_FOR_PICKUP = "READY_FOR_PICKUP"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class OrderItem(BaseModel):
    menu_id: str
    name: str
    price: float
    quantity: int
    subtotal: float


class Order(BaseModel):
    user_id: str
    items: list[OrderItem]
    total_amount: float
    status: OrderStatus = OrderStatus.PLACED
    delivery_address: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    delivery_address: str = Field(
        min_length=5,
        max_length=200
    )


class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: list
    total_amount: float
    status: str
    delivery_address: str
    created_at: str
    updated_at: str


class OrderStatusUpdate(BaseModel):
    status: str
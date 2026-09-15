from pydantic import BaseModel

from app.models.payment import PaymentMethod


class PaymentCreate(BaseModel):
    order_id: str
    payment_method: PaymentMethod


class PaymentStatusUpdate(BaseModel):
    status: str
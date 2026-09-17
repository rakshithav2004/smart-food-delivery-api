from pydantic import BaseModel, Field

class NotificationCreate(BaseModel):
    user_id: str
    type: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=1, max_length=500)
    order_id: str | None = None
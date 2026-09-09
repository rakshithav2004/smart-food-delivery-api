from pydantic import BaseModel, Field

class AddCartItemRequest(BaseModel):
    menu_id: str
    quantity: int = Field(gt=0)

class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(gt=0)
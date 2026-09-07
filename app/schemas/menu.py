from pydantic import BaseModel, Field


class MenuItemCreate(BaseModel):
    restaurant_id: str
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None
    price: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=50)


class MenuItemUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: str | None = None
    price: float | None = Field(
        default=None,
        gt=0
    )
    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    is_available: bool | None = None


class MenuItemResponse(BaseModel):
    id: str
    restaurant_id: str
    name: str
    description: str | None
    price: float
    category: str
    is_available: bool
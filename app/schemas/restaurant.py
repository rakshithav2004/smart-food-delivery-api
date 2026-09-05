from pydantic import BaseModel, Field


class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None
    address: str = Field(min_length=5, max_length=200)
    cuisine: str = Field(min_length=2, max_length=50)


class RestaurantResponse(BaseModel):
    id: str
    name: str
    description: str | None
    address: str
    cuisine: str
    owner_id: str
    is_active: bool

class RestaurantUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: str | None = None
    address: str | None = Field(
        default=None,
        min_length=5,
        max_length=200
    )
    cuisine: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    is_active: bool | None = None    
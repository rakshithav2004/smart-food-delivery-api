from pydantic import BaseModel, Field

class DeliveryPartnerCreate(BaseModel):
    phone: str = Field(
        min_length=10,
        max_length=15
    )
    vehicle_type: str = Field(
        min_length=2,
        max_length=30
    )
    vehicle_number: str = Field(
        min_length=4,
        max_length=20
    )

class DeliveryAvailabilityUpdate(BaseModel):
    is_available: bool
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import require_roles
from app.schemas.delivery import (
    DeliveryPartnerCreate,
    DeliveryAvailabilityUpdate
)
from app.services.delivery_service import delivery_service


router = APIRouter(
    prefix="/api/v1/delivery",
    tags=["Delivery"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_delivery_partner(
    partner_data: DeliveryPartnerCreate,
    current_user: dict = Depends(
        require_roles("DELIVERY_PARTNER")
    )
):
    try:
        return await delivery_service.register_partner(
            user_id=current_user["user_id"],
            partner_data=partner_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/profile")
async def get_delivery_profile(
    current_user: dict = Depends(
        require_roles("DELIVERY_PARTNER")
    )
):
    try:
        return await delivery_service.get_my_profile(
            current_user["user_id"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/availability")
async def update_availability(
    availability_data: DeliveryAvailabilityUpdate,
    current_user: dict = Depends(
        require_roles("DELIVERY_PARTNER")
    )
):
    try:
        return await delivery_service.update_availability(
            user_id=current_user["user_id"],
            is_available=availability_data.is_available
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/available")
async def get_available_partners(
    current_user: dict = Depends(
        require_roles("RESTAURANT_OWNER", "ADMIN")
    )
):
    return await delivery_service.get_available_partners()
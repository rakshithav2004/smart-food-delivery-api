from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import require_roles
from app.services.restaurant_service import restaurant_service
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate
)


router = APIRouter(
    prefix="/api/v1/restaurants",
    tags=["Restaurants"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    restaurant_data: RestaurantCreate,
    current_user: dict = Depends(
        require_roles("RESTAURANT_OWNER", "ADMIN")
    )
):
    try:
        return await restaurant_service.create_restaurant(
            restaurant_data,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{restaurant_id}")
async def update_restaurant(
    restaurant_id: str,
    update_data: RestaurantUpdate,
    current_user: dict = Depends(
        require_roles("RESTAURANT_OWNER", "ADMIN")
    )
):
    try:
        return await restaurant_service.update_restaurant(
            restaurant_id,
            update_data,
            current_user
        )

    except (ValueError, PermissionError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    try:
        return await restaurant_service.get_restaurant(restaurant_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )  

@router.get("")
async def get_all_restaurants():
    return await restaurant_service.get_all_restaurants()      

@router.put("/{restaurant_id}")
async def update_restaurant(
    restaurant_id: str,
    update_data: RestaurantUpdate,
    current_user: dict = Depends(
        require_roles("RESTAURANT_OWNER", "ADMIN")
    )
):
    try:
        return await restaurant_service.update_restaurant(
            restaurant_id,
            update_data,
            current_user
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: str,
    current_user: dict = Depends(
        require_roles("RESTAURANT_OWNER", "ADMIN")
    )
):
    try:
        return await restaurant_service.delete_restaurant(
            restaurant_id,
            current_user
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )    
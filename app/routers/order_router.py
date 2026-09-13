from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user, require_roles
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.services.order_service import order_service


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(
        require_roles("CUSTOMER")
    )
):
    try:
        return await order_service.create_order(
            user_id=current_user["user_id"],
            delivery_address=order_data.delivery_address
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("")
async def get_my_orders(
    current_user: dict = Depends(
        require_roles("CUSTOMER")
    )
):
    return await order_service.get_my_orders(
        current_user["user_id"]
    )


@router.get("/all")
async def get_all_orders(
    current_user: dict = Depends(
        require_roles(
            "RESTAURANT_OWNER",
            "ADMIN"
        )
    )
):
    return await order_service.get_all_orders()


@router.get("/{order_id}")
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        return await order_service.get_order(
            order_id=order_id,
            user_id=current_user["user_id"]
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


@router.put("/{order_id}/status")
async def update_order_status(
    order_id: str,
    status_data: OrderStatusUpdate,
    current_user: dict = Depends(
        require_roles(
            "RESTAURANT_OWNER",
            "ADMIN"
        )
    )
):
    try:
        return await order_service.update_order_status(
            order_id=order_id,
            new_status=status_data.status
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/cancel")
async def cancel_order(
    order_id: str,
    current_user: dict = Depends(
        require_roles("CUSTOMER")
    )
):
    try:
        return await order_service.cancel_order(
            order_id=order_id,
            user_id=current_user["user_id"]
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
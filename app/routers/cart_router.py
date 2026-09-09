from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import require_roles
from app.schemas.cart import (
    AddCartItemRequest,
    UpdateCartItemRequest
)
from app.services.cart_service import cart_service


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"]
)


@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_cart_item(
    cart_data: AddCartItemRequest,
    current_user: dict = Depends(
        require_roles("CUSTOMER")
    )
):
    try:
        return await cart_service.add_item(
            user_id=current_user["user_id"],
            menu_id=cart_data.menu_id,
            quantity=cart_data.quantity
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("")
async def get_cart(
    current_user: dict = Depends(
        require_roles("CUSTOMER")
    )
):
    return await cart_service.get_cart(
        current_user["user_id"]
    )


@router.put("/items/{menu_id}")
async def update_cart_item(
    menu_id: str,
    cart_data: UpdateCartItemRequest,
    current_user: dict = Depends(
        require_roles("CUSTOMER")
    )
):
    try:
        return await cart_service.update_item(
            user_id=current_user["user_id"],
            menu_id=menu_id,
            quantity=cart_data.quantity
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/items/{menu_id}")
async def remove_cart_item(
    menu_id: str,
    current_user: dict = Depends(
        require_roles("CUSTOMER")
    )
):
    try:
        return await cart_service.remove_item(
            user_id=current_user["user_id"],
            menu_id=menu_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("")
async def clear_cart(
    current_user: dict = Depends(
        require_roles("CUSTOMER")
    )
):
    try:
        return await cart_service.clear_cart(
            current_user["user_id"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
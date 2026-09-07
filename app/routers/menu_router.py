from fastapi import APIRouter, Depends, HTTPException, status

import app
from app.core.security import require_roles
from app.schemas.menu import MenuItemCreate, MenuItemUpdate
from app.services.menu_service import menu_service


router = APIRouter(
    prefix="/api/v1/menu",
    tags=["Menu"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_menu_item(
    menu_data: MenuItemCreate,
    current_user: dict = Depends(
        require_roles("RESTAURANT_OWNER", "ADMIN")
    )
):
    try:
        return await menu_service.create_menu_item(
            menu_data,
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


@router.get("/restaurant/{restaurant_id}")
async def get_restaurant_menu(restaurant_id: str):
    return await menu_service.get_restaurant_menu(
        restaurant_id
    )


@router.get("/{menu_id}")
async def get_menu_item(menu_id: str):
    try:
        return await menu_service.get_menu_item(menu_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{menu_id}")
async def update_menu_item(
    menu_id: str,
    update_data: MenuItemUpdate,
    current_user: dict = Depends(
        require_roles("RESTAURANT_OWNER", "ADMIN")
    )
):
    try:
        return await menu_service.update_menu_item(
            menu_id,
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


@router.delete("/{menu_id}")
async def delete_menu_item(
    menu_id: str,
    current_user: dict = Depends(
        require_roles("RESTAURANT_OWNER", "ADMIN")
    )
):
    try:
        return await menu_service.delete_menu_item(
            menu_id,
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
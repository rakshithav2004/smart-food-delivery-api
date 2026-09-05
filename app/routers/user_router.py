from fastapi import APIRouter, Depends

from app.core.security import get_current_user, require_roles
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import RoleUpdate
from app.services.auth_service import auth_service


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user_id": current_user["user_id"],
        "role": current_user["role"]
    }


@router.get("/admin-test")
async def admin_test(
    current_user: dict = Depends(require_roles("ADMIN"))
):
    return {
        "message": "Welcome Admin",
        "user_id": current_user["user_id"],
        "role": current_user["role"]
    }

@router.put("/{user_id}/role")
async def update_user_role(
    user_id: str,
    role_data: RoleUpdate,
    current_user: dict = Depends(
        require_roles("ADMIN")
    )
):
    try:
        return await auth_service.update_user_role(
            user_id,
            role_data.role.value
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
from fastapi import APIRouter, Depends

from app.core.security import get_current_user, require_roles


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
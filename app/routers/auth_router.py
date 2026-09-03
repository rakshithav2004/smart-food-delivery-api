from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreate
from app.services.auth_service import auth_service

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    try:
        return await auth_service.register_user(user_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
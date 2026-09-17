from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import require_roles
from app.schemas.notification import NotificationCreate
from app.services.notification_service import notification_service

router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["Notifications"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: dict = Depends(require_roles("ADMIN"))
):
    try:
        return await notification_service.create_notification(
        user_id=notification_data.user_id,
        notification_type=notification_data.type,
        message=notification_data.message,
        order_id=notification_data.order_id
    )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("")
async def get_notifications(
    current_user: dict = Depends(require_roles("CUSTOMER"))
):
    return await notification_service.get_user_notifications(
        current_user["user_id"]
    )


@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    current_user: dict = Depends(require_roles("CUSTOMER"))
):
    try:
        return await notification_service.mark_as_read(
            notification_id=notification_id,
            user_id=current_user["user_id"]
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: dict = Depends(require_roles("CUSTOMER"))
):
    try:
        return await notification_service.delete_notification(
            notification_id=notification_id,
            user_id=current_user["user_id"]
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
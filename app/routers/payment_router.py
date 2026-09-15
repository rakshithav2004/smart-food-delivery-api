from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user, require_roles
from app.schemas.payment import PaymentCreate, PaymentStatusUpdate
from app.services.payment_service import payment_service

router = APIRouter(
    prefix="/api/v1/payments",
    tags=["Payments"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: dict = Depends(require_roles("CUSTOMER"))
):
    try:
        return await payment_service.create_payment(
            user_id=current_user["user_id"],
            order_id=payment_data.order_id,
            payment_method=payment_data.payment_method.value
        )

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{payment_id}")
async def get_payment(
    payment_id: str,
    current_user: dict = Depends(require_roles("CUSTOMER"))
):
    try:
        return await payment_service.get_payment(
            payment_id=payment_id,
            user_id=current_user["user_id"]
        )

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/order/{order_id}")
async def get_order_payment(
    order_id: str,
    current_user: dict = Depends(require_roles("CUSTOMER"))
):
    try:
        return await payment_service.get_order_payment(
            order_id=order_id,
            user_id=current_user["user_id"]
        )

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{payment_id}/status")
async def update_payment_status(
    payment_id: str,
    status_data: PaymentStatusUpdate,
    current_user: dict = Depends(require_roles("ADMIN"))
):
    try:
        return await payment_service.update_payment_status(
            payment_id=payment_id,
            new_status=status_data.status
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{payment_id}/refund")
async def refund_payment(
    payment_id: str,
    current_user: dict = Depends(require_roles("ADMIN"))
):
    try:
        return await payment_service.refund_payment(payment_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
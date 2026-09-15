from datetime import datetime, timezone
from uuid import uuid4

from bson import ObjectId

from app.repositories.payment_repository import payment_repository
from app.repositories.order_repository import order_repository


class PaymentService:

    async def create_payment(
        self,
        user_id: str,
        order_id: str,
        payment_method: str
    ):
        # 1. Validate order ID
        try:
            object_id = ObjectId(order_id)
        except Exception:
            raise ValueError("Invalid order ID")

        # 2. Find the order
        order = await order_repository.find_by_id(
            object_id
        )

        if not order:
            raise ValueError("Order not found")

        # 3. Make sure the order belongs to the customer
        if order["user_id"] != user_id:
            raise PermissionError(
                "You are not authorized to pay for this order"
            )

        # 4. Check whether payment already exists
        existing_payment = (
            await payment_repository.find_by_order_id(
                order_id
            )
        )

        if existing_payment:
            raise ValueError(
                "Payment already exists for this order"
            )

        # 5. Don't allow payment for cancelled orders
        if order["status"] == "CANCELLED":
            raise ValueError(
                "Cannot make payment for a cancelled order"
            )

        # 6. Get amount from the order
        amount = order["total_amount"]

        # 7. Generate mock transaction ID
        transaction_id = (
            f"TXN-{uuid4().hex[:10].upper()}"
        )

        now = datetime.now(timezone.utc)

        # 8. Create payment
        payment_document = {
            "order_id": order_id,
            "user_id": user_id,
            "amount": amount,
            "payment_method": payment_method,
            "status": "PENDING",
            "transaction_id": transaction_id,
            "created_at": now,
            "updated_at": now
        }

        payment_id = await payment_repository.create(
            payment_document
        )

        return self._to_response(
            {
                "_id": payment_id,
                **payment_document
            }
        )

    async def get_payment(
        self,
        payment_id: str,
        user_id: str
    ):
        try:
            object_id = ObjectId(payment_id)
        except Exception:
            raise ValueError("Invalid payment ID")

        payment = await payment_repository.find_by_id(
            object_id
        )

        if not payment:
            raise ValueError("Payment not found")

        if payment["user_id"] != user_id:
            raise PermissionError(
                "You are not authorized to view this payment"
            )

        return self._to_response(payment)

    async def get_order_payment(
        self,
        order_id: str,
        user_id: str
    ):
        payment = await payment_repository.find_by_order_id(
            order_id
        )

        if not payment:
            raise ValueError(
                "Payment not found for this order"
            )

        if payment["user_id"] != user_id:
            raise PermissionError(
                "You are not authorized to view this payment"
            )

        return self._to_response(payment)

    async def update_payment_status(
        self,
        payment_id: str,
        new_status: str
    ):
        valid_statuses = {
            "PENDING",
            "SUCCESS",
            "FAILED",
            "REFUNDED"
        }

        if new_status not in valid_statuses:
            raise ValueError(
                f"Invalid payment status: {new_status}"
            )

        try:
            object_id = ObjectId(payment_id)
        except Exception:
            raise ValueError("Invalid payment ID")

        payment = await payment_repository.find_by_id(
            object_id
        )

        if not payment:
            raise ValueError("Payment not found")

        current_status = payment["status"]

        allowed_transitions = {
            "PENDING": {
                "SUCCESS",
                "FAILED"
            },
            "SUCCESS": {
                "REFUNDED"
            },
            "FAILED": set(),
            "REFUNDED": set()
        }

        if new_status not in allowed_transitions.get(
            current_status,
            set()
        ):
            raise ValueError(
                f"Cannot change payment status "
                f"from {current_status} to {new_status}"
            )

        await payment_repository.update(
            object_id,
            {
                "status": new_status,
                "updated_at": datetime.now(timezone.utc)
            }
        )

        updated_payment = (
            await payment_repository.find_by_id(
                object_id
            )
        )

        return self._to_response(updated_payment)

    async def refund_payment(
        self,
        payment_id: str
    ):
        try:
            object_id = ObjectId(payment_id)
        except Exception:
            raise ValueError("Invalid payment ID")

        payment = await payment_repository.find_by_id(
            object_id
        )

        if not payment:
            raise ValueError("Payment not found")

        if payment["status"] != "SUCCESS":
            raise ValueError(
                "Only successful payments can be refunded"
            )

        await payment_repository.update(
            object_id,
            {
                "status": "REFUNDED",
                "updated_at": datetime.now(timezone.utc)
            }
        )

        return {
            "message": "Payment refunded successfully",
            "payment_id": payment_id
        }

    def _to_response(self, payment):
        return {
            "id": str(payment["_id"]),
            "order_id": payment["order_id"],
            "user_id": payment["user_id"],
            "amount": payment["amount"],
            "payment_method": payment["payment_method"],
            "status": payment["status"],
            "transaction_id": payment["transaction_id"],
            "created_at": payment["created_at"],
            "updated_at": payment["updated_at"]
        }


payment_service = PaymentService()
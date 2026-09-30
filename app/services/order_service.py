from datetime import datetime, timezone

from bson import ObjectId

from app.repositories.order_repository import order_repository
from app.repositories.cart_repository import cart_repository


class OrderService:

    async def create_order(
        self,
        user_id: str,
        delivery_address: str
    ):
        # 1. Get the customer's cart
        cart = await cart_repository.find_by_user_id(user_id)

        if not cart:
            raise ValueError("Cart is empty")

        if not cart.get("items"):
            raise ValueError("Cart is empty")

        # 2. Convert cart items into order items
        order_items = []

        for item in cart["items"]:
            order_items.append({
                "menu_id": item["menu_id"],
                "name": item["name"],
                "price": item["price"],
                "quantity": item["quantity"],
                "subtotal": item["subtotal"]
            })

        # 3. Calculate total
        total_amount = sum(
            item["subtotal"]
            for item in order_items
        )

        # 4. Create order document
        now = datetime.now(timezone.utc)

        order_document = {
            "user_id": user_id,
            "items": order_items,
            "total_amount": total_amount,
            "status": "PLACED",
            "delivery_address": delivery_address,
            "created_at": now,
            "updated_at": now
        }

        # 5. Save order to MongoDB
        order_id = await order_repository.create(
            order_document
        )

        # 6. Clear customer's cart
        await cart_repository.delete(user_id)

        # 7. Return created order
        return {
            "id": str(order_id),
            "user_id": user_id,
            "items": order_items,
            "total_amount": total_amount,
            "status": "PLACED",
            "delivery_address": delivery_address,
            "created_at": now,
            "updated_at": now
        }

    async def get_order(
        self,
        order_id: str,
        user_id: str
    ):
        try:
            object_id = ObjectId(order_id)
        except Exception:
            raise ValueError("Invalid order ID")

        order = await order_repository.find_by_id(
            object_id
        )

        if not order:
            raise ValueError("Order not found")

        # Customer can only see their own order
        if order["user_id"] != user_id:
            raise PermissionError(
                "You are not authorized to view this order"
            )

        return self._to_response(order)

    async def get_my_orders(
        self,
        user_id: str
    ):
        orders = await order_repository.find_by_user_id(
            user_id
        )

        return [
            self._to_response(order)
            for order in orders
        ]

    async def get_all_orders(self):
        orders = await order_repository.find_all()

        return [
            self._to_response(order)
            for order in orders
        ]

    async def update_order_status(
        self,
        order_id: str,
        new_status: str
    ):
        valid_statuses = {
            "PLACED",
            "CONFIRMED",
            "PREPARING",
            "READY_FOR_PICKUP",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "CANCELLED"
        }

        if new_status not in valid_statuses:
            raise ValueError(
                f"Invalid order status: {new_status}"
            )

        try:
            object_id = ObjectId(order_id)
        except Exception:
            raise ValueError("Invalid order ID")

        order = await order_repository.find_by_id(
            object_id
        )

        if not order:
            raise ValueError("Order not found")

        current_status = order["status"]

        # Don't allow changes after delivery
        if current_status == "DELIVERED":
            raise ValueError(
                "Delivered order cannot be updated"
            )

        # Don't allow changes after cancellation
        if current_status == "CANCELLED":
            raise ValueError(
                "Cancelled order cannot be updated"
            )

        # Customer/restaurant workflow validation
        allowed_transitions = {
            "PLACED": {
                "CONFIRMED",
                "CANCELLED"
            },
            "CONFIRMED": {
                "PREPARING",
                "CANCELLED"
            },
            "PREPARING": {
                "READY_FOR_PICKUP"
            },
            "READY_FOR_PICKUP": {
                "OUT_FOR_DELIVERY"
            },
            "OUT_FOR_DELIVERY": {
                "DELIVERED"
            }
        }

        if new_status not in allowed_transitions.get(
            current_status,
            set()
        ):
            raise ValueError(
                f"Cannot change order status "
                f"from {current_status} to {new_status}"
            )

        await order_repository.update_status(
            object_id,
            new_status
        )

        updated_order = await order_repository.find_by_id(
            object_id
        )

        return self._to_response(updated_order)

    async def cancel_order(
        self,
        order_id: str,
        user_id: str
    ):
        try:
            object_id = ObjectId(order_id)
        except Exception:
            raise ValueError("Invalid order ID")

        order = await order_repository.find_by_id(
            object_id
        )

        if not order:
            raise ValueError("Order not found")

        if order["user_id"] != user_id:
            raise PermissionError(
                "You are not authorized to cancel this order"
            )

        if order["status"] not in {
            "PLACED",
            "CONFIRMED"
        }:
            raise ValueError(
                "Order cannot be cancelled at this stage"
            )

        await order_repository.update_status(
            object_id,
            "CANCELLED"
        )

        return {
            "message": "Order cancelled successfully",
            "order_id": order_id
        }

    def _to_response(self, order):
        return {
            "id": str(order["_id"]),
            "user_id": order["user_id"],
            "items": order["items"],
            "total_amount": order["total_amount"],
            "status": order["status"],
            "delivery_address": order["delivery_address"],
            "created_at": order["created_at"],
            "updated_at": order["updated_at"]
        }


order_service = OrderService()
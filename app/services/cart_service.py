from datetime import datetime, timezone

from bson import ObjectId

from app.repositories.cart_repository import cart_repository
from app.repositories.menu_repository import menu_repository


class CartService:

    async def add_item(
        self,
        user_id: str,
        menu_id: str,
        quantity: int
    ):
        # Find menu item
        menu_item = await menu_repository.find_by_id(
            ObjectId(menu_id)
        )

        if not menu_item:
            raise ValueError("Menu item not found")

        # Check availability
        if not menu_item["is_available"]:
            raise ValueError("Menu item is currently unavailable")

        # Get existing cart
        cart = await cart_repository.find_by_user_id(user_id)

        if not cart:
            # Create a new cart
            subtotal = menu_item["price"] * quantity

            cart_data = {
                "user_id": user_id,
                "items": [
                    {
                        "menu_id": menu_id,
                        "name": menu_item["name"],
                        "price": menu_item["price"],
                        "quantity": quantity,
                        "subtotal": subtotal
                    }
                ],
                "total_amount": subtotal,
                "updated_at": datetime.now(timezone.utc)
            }

            await cart_repository.create(cart_data)

            return cart_data

        # Check whether item already exists
        item_found = False

        for item in cart["items"]:
            if item["menu_id"] == menu_id:
                item["quantity"] += quantity
                item["subtotal"] = (
                    item["price"] * item["quantity"]
                )
                item_found = True
                break

        # Add new item if it doesn't exist
        if not item_found:
            cart["items"].append({
                "menu_id": menu_id,
                "name": menu_item["name"],
                "price": menu_item["price"],
                "quantity": quantity,
                "subtotal": menu_item["price"] * quantity
            })

        # Recalculate total
        total_amount = sum(
            item["subtotal"]
            for item in cart["items"]
        )

        update_data = {
            "items": cart["items"],
            "total_amount": total_amount,
            "updated_at": datetime.now(timezone.utc)
        }

        await cart_repository.update(
            user_id,
            update_data
        )

        return {
            "user_id": user_id,
            **update_data
        }

    async def get_cart(self, user_id: str):
        cart = await cart_repository.find_by_user_id(user_id)

        if not cart:
            return {
                "user_id": user_id,
                "items": [],
                "total_amount": 0.0
            }

        return {
            "user_id": cart["user_id"],
            "items": cart["items"],
            "total_amount": cart["total_amount"],
            "updated_at": cart.get("updated_at")
        }

    async def update_item(
        self,
        user_id: str,
        menu_id: str,
        quantity: int
    ):
        cart = await cart_repository.find_by_user_id(user_id)

        if not cart:
            raise ValueError("Cart not found")

        item_found = False

        for item in cart["items"]:
            if item["menu_id"] == menu_id:
                item["quantity"] = quantity
                item["subtotal"] = (
                    item["price"] * quantity
                )
                item_found = True
                break

        if not item_found:
            raise ValueError("Menu item is not in the cart")

        total_amount = sum(
            item["subtotal"]
            for item in cart["items"]
        )

        update_data = {
            "items": cart["items"],
            "total_amount": total_amount,
            "updated_at": datetime.now(timezone.utc)
        }

        await cart_repository.update(
            user_id,
            update_data
        )

        return {
            "user_id": user_id,
            **update_data
        }

    async def remove_item(
        self,
        user_id: str,
        menu_id: str
    ):
        cart = await cart_repository.find_by_user_id(user_id)

        if not cart:
            raise ValueError("Cart not found")

        original_count = len(cart["items"])

        cart["items"] = [
            item
            for item in cart["items"]
            if item["menu_id"] != menu_id
        ]

        if len(cart["items"]) == original_count:
            raise ValueError("Menu item is not in the cart")

        total_amount = sum(
            item["subtotal"]
            for item in cart["items"]
        )

        update_data = {
            "items": cart["items"],
            "total_amount": total_amount,
            "updated_at": datetime.now(timezone.utc)
        }

        await cart_repository.update(
            user_id,
            update_data
        )

        return {
            "user_id": user_id,
            **update_data
        }

    async def clear_cart(self, user_id: str):
        deleted = await cart_repository.delete(user_id)

        if deleted == 0:
            raise ValueError("Cart not found")

        return {
            "message": "Cart cleared successfully",
            "user_id": user_id
        }


cart_service = CartService()
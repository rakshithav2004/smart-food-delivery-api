from bson import ObjectId

from app.models import restaurant
from app.models import restaurant
from app.repositories.menu_repository import menu_repository
from app.repositories.restaurant_repository import restaurant_repository


class MenuService:

    async def create_menu_item(self, menu_data, current_user):
        # Check if restaurant exists
        restaurant = await restaurant_repository.find_by_id(
            ObjectId(menu_data.restaurant_id)
        )

        if not restaurant:
            raise ValueError("Restaurant not found")

        # Only restaurant owner or ADMIN can add menu items
        if (
            restaurant["owner_id"] != current_user["user_id"]
            and current_user["role"] != "ADMIN"
        ):
            raise PermissionError(
                "You are not authorized to manage this restaurant's menu"
            )

        menu_document = {
            "restaurant_id": menu_data.restaurant_id,
            "name": menu_data.name,
            "description": menu_data.description,
            "price": menu_data.price,
            "category": menu_data.category,
            "is_available": True
        }

        menu_id = await menu_repository.create(menu_document)

        return {
            "id": str(menu_id),
            "restaurant_id": menu_data.restaurant_id,
            "name": menu_data.name,
            "description": menu_data.description,
            "price": menu_data.price,
            "category": menu_data.category,
            "is_available": True
        }

    async def get_menu_item(self, menu_id: str):
        menu_item = await menu_repository.find_by_id(
            ObjectId(menu_id)
        )

        if not menu_item:
            raise ValueError("Menu item not found")

        return {
            "id": str(menu_item["_id"]),
            "restaurant_id": menu_item["restaurant_id"],
            "name": menu_item["name"],
            "description": menu_item.get("description"),
            "price": menu_item["price"],
            "category": menu_item["category"],
            "is_available": menu_item["is_available"]
        }

    async def get_restaurant_menu(self, restaurant_id: str):
        items = await menu_repository.find_by_restaurant(
            restaurant_id
        )

        return [
            {
                "id": str(item["_id"]),
                "restaurant_id": item["restaurant_id"],
                "name": item["name"],
                "description": item.get("description"),
                "price": item["price"],
                "category": item["category"],
                "is_available": item["is_available"]
            }
            for item in items
        ]

    async def update_menu_item(
        self,
        menu_id: str,
        update_data,
        current_user: dict
    ):
        menu_item = await menu_repository.find_by_id(
            ObjectId(menu_id)
        )

        if not menu_item:
            raise ValueError("Menu item not found")

        restaurant = await restaurant_repository.find_by_id(
        ObjectId(menu_item["restaurant_id"])
        )

        if not restaurant:
            raise ValueError("Restaurant not found")

        if (
            restaurant["owner_id"] != current_user["user_id"]
            and current_user["role"] != "ADMIN"
        ):
            raise PermissionError(
                "You are not authorized to update this menu item"
            )

        update_fields = update_data.model_dump(exclude_unset=True)

        if not update_fields:
            raise ValueError("No fields provided for update")

        await menu_repository.update(
            ObjectId(menu_id),
            update_fields
        )

        updated_item = await menu_repository.find_by_id(
            ObjectId(menu_id)
        )

        return {
        "id": str(updated_item["_id"]),
        "restaurant_id": updated_item["restaurant_id"],
        "name": updated_item["name"],
        "description": updated_item.get("description"),
        "price": updated_item["price"],
        "category": updated_item["category"],
        "is_available": updated_item["is_available"]
        }


    async def delete_menu_item(
        self,
        menu_id: str,
        current_user: dict
    ):
        menu_item = await menu_repository.find_by_id(
            ObjectId(menu_id)
        )

        if not menu_item:
            raise ValueError("Menu item not found")

        restaurant = await restaurant_repository.find_by_id(
            ObjectId(menu_item["restaurant_id"])
        )

        if not restaurant:
            raise ValueError("Restaurant not found")

        if (
            restaurant["owner_id"] != current_user["user_id"]
            and current_user["role"] != "ADMIN"
        ):
            raise PermissionError(
                "You are not authorized to delete this menu item"
            )

        deleted = await menu_repository.delete(
            ObjectId(menu_id)
        )

        if deleted == 0:
            raise ValueError("Menu item could not be deleted")

        return {
            "message": "Menu item deleted successfully",
            "menu_id": menu_id
        }

    async def search_menu_items(
        self,
        restaurant_id: str | None = None,
        name: str | None = None,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        is_available: bool | None = None
    ):
        items = await menu_repository.search(
            restaurant_id=restaurant_id,
            name=name,
            category=category,
            min_price=min_price,
            max_price=max_price,
            is_available=is_available
        )

        return [
            {
                "id": str(item["_id"]),
                "restaurant_id": item["restaurant_id"],
                "name": item["name"],
                "description": item.get("description"),
                "price": item["price"],
                "category": item["category"],
                "is_available": item["is_available"]
            }
            for item in items
        ]


menu_service = MenuService()
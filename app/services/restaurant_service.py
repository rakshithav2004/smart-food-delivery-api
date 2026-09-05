from bson import ObjectId

from app.models import restaurant
from app.repositories.restaurant_repository import restaurant_repository
from app.schemas import restaurant


class RestaurantService:

    async def create_restaurant(self, restaurant_data, current_user):
        restaurant_document = {
            "name": restaurant_data.name,
            "description": restaurant_data.description,
            "address": restaurant_data.address,
            "cuisine": restaurant_data.cuisine,
            "owner_id": current_user["user_id"],
            "is_active": True
        }

        restaurant_id = await restaurant_repository.create(
            restaurant_document
        )

        return {
            "id": str(restaurant_id),
            "name": restaurant_data.name,
            "description": restaurant_data.description,
            "address": restaurant_data.address,
            "cuisine": restaurant_data.cuisine,
            "owner_id": current_user["user_id"],
            "is_active": True
        }

    async def get_restaurant(self, restaurant_id: str):
        restaurant = await restaurant_repository.find_by_id(
            ObjectId(restaurant_id)
        )

        if not restaurant:
            raise ValueError("Restaurant not found")

        return {
            "id": str(restaurant["_id"]),
            "name": restaurant["name"],
            "description": restaurant.get("description"),
            "address": restaurant["address"],
            "cuisine": restaurant["cuisine"],
            "owner_id": restaurant["owner_id"],
            "is_active": restaurant["is_active"]
        }

    async def get_all_restaurants(self):
        restaurants = await restaurant_repository.find_all()

        return [
        {
            "id": str(restaurant["_id"]),
            "name": restaurant["name"],
            "description": restaurant.get("description"),
            "address": restaurant["address"],
            "cuisine": restaurant["cuisine"],
            "owner_id": restaurant["owner_id"],
            "is_active": restaurant["is_active"]
        }
        for restaurant in restaurants
    ]

    async def update_restaurant(
    self,
    restaurant_id: str,
    update_data,
    current_user: dict):
        restaurant = await restaurant_repository.find_by_id(
            ObjectId(restaurant_id)
        )

        if not restaurant:
            raise ValueError("Restaurant not found")

    # Only the owner or ADMIN can update
        if (
            restaurant["owner_id"] != current_user["user_id"]
            and current_user["role"] != "ADMIN"
        ):
            raise PermissionError(
                "You are not authorized to update this restaurant"
            )

        update_fields = update_data.model_dump(
            exclude_unset=True
        )

        if not update_fields:
            raise ValueError("No fields provided for update")

        await restaurant_repository.update(
            ObjectId(restaurant_id),
            update_fields
        )

        updated_restaurant = await restaurant_repository.find_by_id(
            ObjectId(restaurant_id)
        )

        return {
            "id": str(updated_restaurant["_id"]),
            "name": updated_restaurant["name"],
            "description": updated_restaurant.get("description"),
            "address": updated_restaurant["address"],
            "cuisine": updated_restaurant["cuisine"],
            "owner_id": updated_restaurant["owner_id"],
            "is_active": updated_restaurant["is_active"]
        }


    async def delete_restaurant(
    self,
    restaurant_id: str,
    current_user: dict):
        restaurant = await restaurant_repository.find_by_id(
            ObjectId(restaurant_id)
        )

        if not restaurant:
            raise ValueError("Restaurant not found")

        # Only the owner or ADMIN can delete
        if (
            restaurant["owner_id"] != current_user["user_id"]
            and current_user["role"] != "ADMIN"
        ):
            raise PermissionError(
                "You are not authorized to delete this restaurant"
            )

        deleted = await restaurant_repository.delete(
            ObjectId(restaurant_id)
        )

        if deleted == 0:
            raise ValueError("Restaurant could not be deleted")

        return {
            "message": "Restaurant deleted successfully",
            "restaurant_id": restaurant_id
        }

restaurant_service = RestaurantService()
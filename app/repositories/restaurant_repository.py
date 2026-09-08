from unittest import result

from app.config.database import db

class RestaurantRepository:

    async def create(self, restaurant_data: dict):
        result = await db.restaurants.insert_one(restaurant_data)
        return result.inserted_id

    async def find_by_id(self, restaurant_id):
        return await db.restaurants.find_one({
            "_id": restaurant_id
        })

    async def find_all(self):
        restaurants = []

        async for restaurant in db.restaurants.find():
            restaurants.append(restaurant)

        return restaurants

    async def update(self, restaurant_id, update_data: dict):
        result = await db.restaurants.update_one(
            {"_id": restaurant_id},
            {"$set": update_data}
        )
        return result.modified_count

    async def delete(self, restaurant_id):
        result = await db.restaurants.delete_one({
            "_id": restaurant_id
        })

        return result.deleted_count

    async def search(
        self,
        name: str | None = None,
        cuisine: str | None = None,
        is_active: bool | None = None
    ):
        query = {}

        if name:
            query["name"] = {
                "$regex": name,
                "$options": "i"
            }

        if cuisine:
            query["cuisine"] = {
                "$regex": cuisine,
                "$options": "i"
            }

        if is_active is not None:
            query["is_active"] = is_active

        restaurants = []

        async for restaurant in db.restaurants.find(query):
            restaurants.append(restaurant)

        return restaurants    

restaurant_repository = RestaurantRepository()
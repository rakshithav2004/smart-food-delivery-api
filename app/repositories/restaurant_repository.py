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

restaurant_repository = RestaurantRepository()
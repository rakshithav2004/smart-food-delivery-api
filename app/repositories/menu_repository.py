from app.config.database import db


class MenuRepository:

    async def create(self, menu_data: dict):
        result = await db.menu_items.insert_one(menu_data)
        return result.inserted_id

    async def find_by_id(self, menu_id):
        return await db.menu_items.find_one({
            "_id": menu_id
        })

    async def find_by_restaurant(self, restaurant_id: str):
        items = []

        async for item in db.menu_items.find({
            "restaurant_id": restaurant_id
        }):
            items.append(item)

        return items


menu_repository = MenuRepository()
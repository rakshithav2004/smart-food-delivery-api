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

    async def search(
        self,
        restaurant_id: str | None = None,
        name: str | None = None,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        is_available: bool | None = None
    ):
        query = {}

        if restaurant_id:
            query["restaurant_id"] = restaurant_id

        if name:
            query["name"] = {
                "$regex": name,
                "$options": "i"
            }

        if category:
            query["category"] = {
                "$regex": category,
                "$options": "i"
            }

        if min_price is not None or max_price is not None:
            query["price"] = {}

            if min_price is not None:
                query["price"]["$gte"] = min_price

            if max_price is not None:
                query["price"]["$lte"] = max_price

        if is_available is not None:
            query["is_available"] = is_available

        items = []

        async for item in db.menu_items.find(query):
            items.append(item)

        return items


menu_repository = MenuRepository()
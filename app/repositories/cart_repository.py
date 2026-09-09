from app.config.database import db

class CartRepository:

    async def find_by_user_id(self, user_id: str):
        return await db.carts.find_one({
            "user_id": user_id
        })

    async def create(self, cart_data: dict):
        result = await db.carts.insert_one(cart_data)
        return result.inserted_id

    async def update(self, user_id: str, update_data: dict):
        result = await db.carts.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count

    async def delete(self, user_id: str):
        result = await db.carts.delete_one({
            "user_id": user_id
        })
        return result.deleted_count


cart_repository = CartRepository()
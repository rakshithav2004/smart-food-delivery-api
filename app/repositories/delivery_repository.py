from app.config.database import db


class DeliveryRepository:

    async def create(self, delivery_data: dict):
        result = await db.delivery_partners.insert_one(
            delivery_data
        )
        return result.inserted_id

    async def find_by_user_id(self, user_id: str):
        return await db.delivery_partners.find_one({
            "user_id": user_id
        })

    async def find_by_id(self, delivery_id):
        return await db.delivery_partners.find_one({
            "_id": delivery_id
        })

    async def find_available_partners(self):
        partners = []

        async for partner in db.delivery_partners.find({
            "is_available": True
        }):
            partners.append(partner)

        return partners

    async def update(self, user_id: str, update_data: dict):
        result = await db.delivery_partners.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count


delivery_repository = DeliveryRepository()
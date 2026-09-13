from app.config.database import db


class OrderRepository:

    async def create(self, order_data: dict):
        result = await db.orders.insert_one(order_data)
        return result.inserted_id

    async def find_by_id(self, order_id):
        return await db.orders.find_one({
            "_id": order_id
        })

    async def find_by_user_id(self, user_id: str):
        orders = []

        async for order in db.orders.find({
            "user_id": user_id
        }).sort("created_at", -1):
            orders.append(order)

        return orders

    async def find_all(self):
        orders = []

        async for order in db.orders.find().sort(
            "created_at",
            -1
        ):
            orders.append(order)

        return orders

    async def update_status(
        self,
        order_id,
        status: str
    ):
        result = await db.orders.update_one(
            {"_id": order_id},
            {
                "$set": {
                    "status": status
                }
            }
        )

        return result.modified_count


order_repository = OrderRepository()
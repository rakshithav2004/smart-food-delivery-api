from app.config.database import db


class PaymentRepository:

    async def create(self, payment_data: dict):
        result = await db.payments.insert_one(
            payment_data
        )
        return result.inserted_id

    async def find_by_id(self, payment_id):
        return await db.payments.find_one({
            "_id": payment_id
        })

    async def find_by_order_id(
        self,
        order_id: str
    ):
        return await db.payments.find_one({
            "order_id": order_id
        })

    async def find_by_user_id(
        self,
        user_id: str
    ):
        payments = []

        async for payment in db.payments.find({
            "user_id": user_id
        }).sort("created_at", -1):
            payments.append(payment)

        return payments

    async def update(
        self,
        payment_id,
        update_data: dict
    ):
        result = await db.payments.update_one(
            {"_id": payment_id},
            {"$set": update_data}
        )

        return result.modified_count


payment_repository = PaymentRepository()
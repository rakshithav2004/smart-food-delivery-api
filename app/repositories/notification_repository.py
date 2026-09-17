from bson import ObjectId
from app.config.database import db

class NotificationRepository:

    async def create(self, notification_data: dict):
        result = await db.notifications.insert_one(notification_data)
        return result.inserted_id

    async def find_by_id(self, notification_id: ObjectId):
        return await db.notifications.find_one({"_id": notification_id})

    async def find_by_user_id(self, user_id: str):
        notifications = []

        async for notification in db.notifications.find(
            {"user_id": user_id}
        ).sort("created_at", -1):
            notifications.append(notification)

        return notifications

    async def mark_as_read(self, notification_id: ObjectId):
        result = await db.notifications.update_one(
            {"_id": notification_id},
            {"$set": {"is_read": True}}
        )

        return result.modified_count

    async def delete(self, notification_id: ObjectId):
        result = await db.notifications.delete_one(
            {"_id": notification_id}
        )

        return result.deleted_count

notification_repository = NotificationRepository()
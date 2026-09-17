from datetime import datetime, timezone
from bson import ObjectId
from app.repositories.notification_repository import notification_repository

class NotificationService:

    async def create_notification(
        self,
        user_id: str,
        notification_type: str,
        message: str,
        order_id: str | None = None
    ):
        notification_document = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "order_id": order_id,
            "is_read": False,
            "created_at": datetime.now(timezone.utc)
        }

        notification_id = await notification_repository.create(
            notification_document
        )

        return self._to_response({
            "_id": notification_id,
            **notification_document
        })

    async def get_user_notifications(self, user_id: str):
        notifications = await notification_repository.find_by_user_id(
            user_id
        )

        return [
            self._to_response(notification)
            for notification in notifications
        ]

    async def mark_as_read(
        self,
        notification_id: str,
        user_id: str
    ):
        object_id = self._validate_object_id(notification_id)

        notification = await notification_repository.find_by_id(
            object_id
        )

        if not notification:
            raise ValueError("Notification not found")

        if notification["user_id"] != user_id:
            raise PermissionError(
                "You are not authorized to update this notification"
            )

        if notification["is_read"]:
            return self._to_response(notification)

        await notification_repository.mark_as_read(object_id)

        updated_notification = await notification_repository.find_by_id(
            object_id
        )

        return self._to_response(updated_notification)

    async def delete_notification(
        self,
        notification_id: str,
        user_id: str
    ):
        object_id = self._validate_object_id(notification_id)

        notification = await notification_repository.find_by_id(
            object_id
        )

        if not notification:
            raise ValueError("Notification not found")

        if notification["user_id"] != user_id:
            raise PermissionError(
                "You are not authorized to delete this notification"
            )

        await notification_repository.delete(object_id)

        return {
            "message": "Notification deleted successfully",
            "notification_id": notification_id
        }

    def _validate_object_id(self, notification_id: str):
        try:
            return ObjectId(notification_id)
        except Exception:
            raise ValueError("Invalid notification ID")

    def _to_response(self, notification):
        return {
            "id": str(notification["_id"]),
            "user_id": notification["user_id"],
            "type": notification["type"],
            "message": notification["message"],
            "order_id": notification.get("order_id"),
            "is_read": notification["is_read"],
            "created_at": notification["created_at"]
        }

notification_service = NotificationService()
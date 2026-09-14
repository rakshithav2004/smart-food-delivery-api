from datetime import datetime, timezone

from app.repositories.delivery_repository import delivery_repository


class DeliveryService:

    async def register_partner(
        self,
        user_id: str,
        partner_data
    ):
        # Check whether this user already has a delivery profile
        existing_partner = await delivery_repository.find_by_user_id(
            user_id
        )

        if existing_partner:
            raise ValueError(
                "Delivery partner profile already exists"
            )

        delivery_document = {
            "user_id": user_id,
            "phone": partner_data.phone,
            "vehicle_type": partner_data.vehicle_type,
            "vehicle_number": partner_data.vehicle_number,
            "is_available": False,
            "created_at": datetime.now(timezone.utc)
        }

        delivery_id = await delivery_repository.create(
            delivery_document
        )

        return {
            "id": str(delivery_id),
            "user_id": user_id,
            "phone": partner_data.phone,
            "vehicle_type": partner_data.vehicle_type,
            "vehicle_number": partner_data.vehicle_number,
            "is_available": False
        }

    async def get_my_profile(self, user_id: str):
        partner = await delivery_repository.find_by_user_id(
            user_id
        )

        if not partner:
            raise ValueError(
                "Delivery partner profile not found"
            )

        return {
            "id": str(partner["_id"]),
            "user_id": partner["user_id"],
            "phone": partner["phone"],
            "vehicle_type": partner["vehicle_type"],
            "vehicle_number": partner["vehicle_number"],
            "is_available": partner["is_available"]
        }

    async def update_availability(
        self,
        user_id: str,
        is_available: bool
    ):
        partner = await delivery_repository.find_by_user_id(
            user_id
        )

        if not partner:
            raise ValueError(
                "Delivery partner profile not found"
            )

        await delivery_repository.update(
            user_id,
            {
                "is_available": is_available,
                "updated_at": datetime.now(timezone.utc)
            }
        )

        return {
            "message": "Availability updated successfully",
            "user_id": user_id,
            "is_available": is_available
        }

    async def get_available_partners(self):
        partners = (
            await delivery_repository.find_available_partners()
        )

        return [
            {
                "id": str(partner["_id"]),
                "user_id": partner["user_id"],
                "phone": partner["phone"],
                "vehicle_type": partner["vehicle_type"],
                "vehicle_number": partner["vehicle_number"],
                "is_available": partner["is_available"]
            }
            for partner in partners
        ]


delivery_service = DeliveryService()
from app.config.database import db

class UserRepository:

    async def find_by_email(self, email: str):
        return await db.users.find_one({"email": email})

    async def create(self, user_data: dict):
        result = await db.users.insert_one(user_data)
        return result.inserted_id

    async def update_role(self, user_id, role: str):
        result = await db.users.update_one(
            {"_id": user_id},
            {"$set": {"role": role}}
        )

        return result.modified_count

    async def find_by_id(self, user_id):
        return await db.users.find_one({"_id": user_id})

user_repository = UserRepository()
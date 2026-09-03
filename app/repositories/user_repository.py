from app.config.database import db


class UserRepository:

    async def find_by_email(self, email: str):
        return await db.users.find_one({"email": email})

    async def create(self, user_data: dict):
        result = await db.users.insert_one(user_data)
        return result.inserted_id


user_repository = UserRepository()
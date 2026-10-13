from pymongo import AsyncMongoClient, ASCENDING
from app.config.settings import settings

client = AsyncMongoClient(settings.mongo_uri)
db = client[settings.database_name]

async def create_indexes():
    """Create indexes required by the application."""
    await db.users.create_index(
        [("email", ASCENDING)],
        unique=True,
        name="unique_user_email"
    )
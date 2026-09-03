from pymongo import AsyncMongoClient

from app.config.settings import settings


client = AsyncMongoClient(settings.mongo_uri)

db = client[settings.database_name]
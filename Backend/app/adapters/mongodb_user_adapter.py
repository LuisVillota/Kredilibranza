from motor.motor_asyncio import AsyncIOMotorClient

from app.configurations import Configs
from app.core.models import UserInDB
from app.core.ports import UserRepositoryPort


class MongoDBUserAdapter(UserRepositoryPort):
    def __init__(self):
        configs = Configs()
        self.client = AsyncIOMotorClient(configs.mongodb_uri)
        self.db = self.client[configs.mongodb_name]

    async def get_user_by_username(self, username: str) -> UserInDB | None:
        user_data = await self.db["users"].find_one({"username": username})
        if user_data:
            return UserInDB(**user_data)
        return None

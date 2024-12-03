from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorClient

from app.configurations import Configs
from app.core.ports import FormRepositoryPort


class MongoDBAdapter(FormRepositoryPort):
    def __init__(self):
        configs = Configs()
        self.client = AsyncIOMotorClient(configs.mongodb_uri)
        self.db = self.client[configs.mongodb_name]
        print("Conexión exitosa a MongoDB")

    async def insert_form_submission(self, data: Dict[str, Any]) -> Any:
        result = await self.db["form_submissions"].insert_one(data)
        return result.inserted_id

    async def get_form_submission(self, submission_id: str) -> Dict[str, Any]:
        document = await self.db["form_submissions"].find_one({"_id": submission_id})
        return document

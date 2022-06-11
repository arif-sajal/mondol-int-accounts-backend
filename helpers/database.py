from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from settings import settings

client = AsyncIOMotorClient(settings.DB_URL)
db = AIOEngine(motor_client=client, database=settings.DB_NAME)

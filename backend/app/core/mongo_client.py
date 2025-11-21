from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

_settings = get_settings()


class MongoClientManager:
    """Mongo client manager for core DB and tenant DBs."""

    def __init__(self) -> None:
        self._client = AsyncIOMotorClient(_settings.MONGO_URI)

    @property
    def client(self) -> AsyncIOMotorClient:
        return self._client

    def get_core_db(self) -> AsyncIOMotorDatabase:
        """Return the core database used to store tenant metadata."""
        return self._client[_settings.CORE_DB_NAME]

    def get_tenant_db(self, db_name: str) -> AsyncIOMotorDatabase:
        """Return a tenant-specific database by name."""
        return self._client[db_name]


mongo_manager = MongoClientManager()

from typing import Optional

from app.core.mongo_client import mongo_manager


async def get_tenant_by_client_number(client_number: int) -> Optional[dict]:
    """Retrieve tenant document from core DB using the client number."""
    core_db = mongo_manager.get_core_db()
    tenant = await core_db.tenants.find_one({"client_number": client_number})
    return tenant


async def get_tenant_by_id(tenant_id: str) -> Optional[dict]:
    """Retrieve tenant document from core DB using the tenant_id."""
    core_db = mongo_manager.get_core_db()
    tenant = await core_db.tenants.find_one({"tenant_id": tenant_id})
    return tenant

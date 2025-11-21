import uuid
import random

from fastapi import APIRouter

from app.api.v1.schemas.tenants import TenantRegisterRequest, TenantRegisterResponse
from app.core.mongo_client import mongo_manager
from app.models.tenant import build_default_tenant_document

router = APIRouter()


@router.post("/register", response_model=TenantRegisterResponse)
async def register_tenant(payload: TenantRegisterRequest) -> TenantRegisterResponse:
    """Register a new tenant (company).

    This endpoint is responsible for:
    - Generating a random 4-digit client_number
    - Generating a random 6-char db_name
    - Creating a tenant-specific Mongo database (implicitly by using it)
    - Inserting a tenant document in core_db.tenants

    The creation of the default admin user and initial collections will be
    implemented in a later iteration.
    """
    core_db = mongo_manager.get_core_db()

    # Generate tenant_id, client_number and db_name
    tenant_id = str(uuid.uuid4())
    client_number = random.randint(1000, 9999)
    db_name = f"tenant_{uuid.uuid4().hex[:6].upper()}"

    tenant_doc = build_default_tenant_document(
        tenant_id=tenant_id,
        client_number=client_number,
        name=payload.name,
        contact_email=payload.contact_email,
        db_name=db_name,
    )

    await core_db.tenants.insert_one(tenant_doc)

    # Touch tenant DB so it is created in Mongo (lazy creation)
    tenant_db = mongo_manager.get_tenant_db(db_name)
    await tenant_db.command("ping")

    return TenantRegisterResponse(
        tenant_id=tenant_id,
        client_number=client_number,
        db_name=db_name,
    )

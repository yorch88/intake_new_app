import uuid
import random

from fastapi import APIRouter

from app.api.v1.schemas.tenants import TenantRegisterRequest, TenantRegisterResponse
from app.core.mongo_client import mongo_manager
from app.core.security import get_password_hash
from app.models.tenant import build_default_tenant_document

router = APIRouter()


@router.post("/register", response_model=TenantRegisterResponse)
async def register_tenant(payload: TenantRegisterRequest) -> TenantRegisterResponse:
    """Register a new tenant (company) and create a default admin user."""

    core_db = mongo_manager.get_core_db()

    # Generate identifiers
    tenant_id = str(uuid.uuid4())
    client_number = random.randint(1000, 9999)
    db_name = f"tenant_{uuid.uuid4().hex[:6].upper()}"

    # Tenant metadata in core_db
    tenant_doc = build_default_tenant_document(
        tenant_id=tenant_id,
        client_number=client_number,
        name=payload.name,
        contact_email=payload.contact_email,
        db_name=db_name,
    )

    await core_db.tenants.insert_one(tenant_doc)

    # Initialize tenant database and create default admin user
    tenant_db = mongo_manager.get_tenant_db(db_name)

    # Ensure DB exists by pinging
    await tenant_db.command("ping")

    # Create default admin user:
    # In a real system, you would either:
    # - Generate a random password and email it, or
    # - Ask for admin credentials during registration.
    default_admin = {
        "username": "admin",
        "role": "admin",
        "password_hash": get_password_hash("admin123"),
        "is_active": True,
    }

    await tenant_db.users.insert_one(default_admin)

    # Optionally create an index on username for faster lookups
    await tenant_db.users.create_index("username", unique=True)

    return TenantRegisterResponse(
        tenant_id=tenant_id,
        client_number=client_number,
        db_name=db_name,
    )

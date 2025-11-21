from typing import Optional
from pydantic import BaseModel, EmailStr


class TenantRegisterRequest(BaseModel):
    """Payload used to register a new company (tenant)."""

    name: str
    industry: Optional[str] = None
    contact_email: EmailStr
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None


class TenantRegisterResponse(BaseModel):
    """Response returned after registering a new tenant."""

    tenant_id: str
    client_number: int
    db_name: str

from typing import Optional
from pydantic import BaseModel, EmailStr


class IntakeRequest(BaseModel):
    """Public intake form payload submitted by end customers."""

    tenant_id: str
    service_type: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    captcha_token: str

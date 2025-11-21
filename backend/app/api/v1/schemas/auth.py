from pydantic import BaseModel


class ResolveTenantRequest(BaseModel):
    """Request used in the first login step to resolve tenant by client number."""

    client_number: int


class ResolveTenantResponse(BaseModel):
    """Response returned after resolving tenant information."""

    tenant_id: str
    name: str
    db_name: str
    layout_option: int
    primary_color: str
    secondary_color: str
    accent_color: str


class LoginRequest(BaseModel):
    """Request used in the second login step to authenticate an admin user."""

    tenant_id: str
    username: str
    password: str


class LoginResponse(BaseModel):
    """Response containing JWT access token."""

    access_token: str
    token_type: str = "bearer"

from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas.auth import (
    ResolveTenantRequest,
    ResolveTenantResponse,
    LoginRequest,
    LoginResponse,
)
from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.core.mongo_client import mongo_manager
from app.core.tenant_resolver import get_tenant_by_client_number, get_tenant_by_id

router = APIRouter()
_settings = get_settings()


@router.post("/resolve-tenant", response_model=ResolveTenantResponse)
async def resolve_tenant(payload: ResolveTenantRequest) -> ResolveTenantResponse:
    """First login step: resolve tenant by client number."""
    tenant = await get_tenant_by_client_number(payload.client_number)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found for given client number",
        )

    layout = tenant.get("layout", {})
    theme_colors = layout.get("colors", {})

    return ResolveTenantResponse(
        tenant_id=str(tenant.get("tenant_id", "")),
        name=tenant.get("name", ""),
        db_name=tenant.get("db_name", ""),
        layout_option=layout.get("option", 1),
        primary_color=theme_colors.get("primary", "#000000"),
        secondary_color=theme_colors.get("secondary", "#ffffff"),
        accent_color=theme_colors.get("accent", "#cccccc"),
    )


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest) -> LoginResponse:
    """Second login step: authenticate an admin user and return a JWT."""
    tenant = await get_tenant_by_id(payload.tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    db_name = tenant.get("db_name")
    if not db_name:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Tenant database not configured",
        )

    tenant_db = mongo_manager.get_tenant_db(db_name)

    user = await tenant_db.users.find_one({"username": payload.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    hashed_password = user.get("password_hash", "")
    if not verify_password(payload.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    user_id = str(user.get("_id"))
    role = user.get("role", "admin")
    access_token = create_access_token(
        subject=user_id,
        tenant_id=str(tenant.get("tenant_id")),
        role=role,
    )

    return LoginResponse(access_token=access_token)

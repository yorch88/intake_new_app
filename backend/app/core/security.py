from datetime import datetime, timedelta
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

_settings = get_settings()

# Use pbkdf2_sha256 to avoid bcrypt backend issues and 72-byte limitations
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storing in the database."""
    return pwd_context.hash(password)


def create_access_token(
    subject: str,
    tenant_id: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=_settings.JWT_EXPIRE_MINUTES)

    to_encode: dict[str, Any] = {
        "sub": subject,
        "tenant_id": tenant_id,
        "role": role,
        "exp": datetime.utcnow() + expires_delta,
    }
    encoded_jwt = jwt.encode(
        to_encode,
        _settings.JWT_SECRET,
        algorithm=_settings.JWT_ALGORITHM,
    )
    return encoded_jwt

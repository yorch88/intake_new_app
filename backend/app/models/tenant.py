"""Tenant model helpers.

With MongoDB we do not enforce a strict schema at database level, but this module
can be used to centralize keys and default structures for tenants.
"""
from typing import Any, Dict


def build_default_tenant_document(
    tenant_id: str,
    client_number: int,
    name: str,
    contact_email: str,
    db_name: str,
) -> Dict[str, Any]:
    """Build a default tenant document for insertion into core_db.tenants."""
    return {
        "tenant_id": tenant_id,
        "client_number": client_number,
        "name": name,
        "contact_email": contact_email,
        "db_name": db_name,
        "status": "active",
        "layout": {
            "option": 1,
            "colors": {
                "primary": "#000000",
                "secondary": "#ffffff",
                "accent": "#cccccc",
            },
            "images": {},
        },
    }

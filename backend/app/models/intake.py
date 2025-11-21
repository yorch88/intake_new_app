"""Intake model helpers for tenant databases."""
from typing import Any, Dict


def build_intake_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize an intake payload before inserting into MongoDB."""
    # For now we simply return the payload.
    # This is a placeholder for future transformations or validations.
    return payload

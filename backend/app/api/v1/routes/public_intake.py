import json
from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas.intake import IntakeRequest
from app.core.redis_client import get_redis_client
from app.core.tenant_resolver import get_tenant_by_id

router = APIRouter()


@router.post("/intake")
async def submit_intake(payload: IntakeRequest):
    """Public endpoint to submit an intake form.

    The intake payload is pushed into Redis and later processed
    by a background worker that persists it into MongoDB and
    sends notification emails.
    """
    # TODO: validate captcha_token with external provider (e.g. reCAPTCHA)

    tenant = await get_tenant_by_id(payload.tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    redis_client = get_redis_client()
    queue_key = f"intake_queue:{payload.tenant_id}"

    intake_dict = payload.dict()
    redis_client.lpush(queue_key, json.dumps(intake_dict))

    return {"status": "queued"}

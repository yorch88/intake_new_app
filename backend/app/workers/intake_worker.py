"""Background worker that processes intake queues from Redis.

This worker should be executed in a separate container or process.
It will:
- read intake items from Redis for each tenant
- insert them into the tenant's MongoDB database
- send notification emails to the company
"""
import asyncio
import json
from typing import List

from app.core.redis_client import get_redis_client
from app.core.mongo_client import mongo_manager
from app.core.tenant_resolver import get_tenant_by_id
from app.core.email import send_email
from app.models.intake import build_intake_document


async def process_intake_queue(tenant_id: str) -> None:
    """Process all intake items for a specific tenant_id."""
    redis_client = get_redis_client()
    queue_key = f"intake_queue:{tenant_id}"

    items: List[str] = []
    while True:
        item = redis_client.rpop(queue_key)
        if item is None:
            break
        items.append(item)

    if not items:
        return

    tenant = await get_tenant_by_id(tenant_id)
    if not tenant:
        return

    db_name = tenant.get("db_name")
    if not db_name:
        return

    tenant_db = mongo_manager.get_tenant_db(db_name)

    intake_docs = []
    for raw in items:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        intake_docs.append(build_intake_document(data))

    if not intake_docs:
        return

    await tenant_db.intakes.insert_many(intake_docs)

    # Send a basic notification email
    to_address = tenant.get("contact_email")
    if to_address:
        subject = "New intake submissions"
        body = f"{len(intake_docs)} new intake(s) have been stored for tenant {tenant_id}."
        send_email(subject, body, [to_address])


async def worker_loop(poll_interval_seconds: int = 300) -> None:
    """Main worker loop that periodically scans Redis for intake queues."""
    redis_client = get_redis_client()

    while True:
        # Discover all intake queues
        keys = redis_client.keys("intake_queue:*")
        tasks = []
        for key in keys:
            _, tenant_id = key.split(":", 1)
            tasks.append(process_intake_queue(tenant_id))

        if tasks:
            await asyncio.gather(*tasks)

        await asyncio.sleep(poll_interval_seconds)


if __name__ == "__main__":
    asyncio.run(worker_loop())

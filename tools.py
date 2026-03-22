import asyncio
import random

async def cancel_order(order_id: str) -> dict:
    """Simulates cancelling an order with a 20% failure rate."""
    if random.random() < 0.20:
        return {"status": "failed", "error": "Order not found or already processed"}
    return {"status": "success", "order_id": order_id}

async def send_email(email: str, message: str) -> dict:
    """Simulates sending an email with a 1-second network delay."""
    await asyncio.sleep(1)
    return {"status": "sent", "to": email}

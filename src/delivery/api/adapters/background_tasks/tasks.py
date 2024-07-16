import asyncio
from typing import Any

from celery import Celery, shared_task

from delivery.config import settings
from delivery.core.application.use_cases.commands.assign_orders import AssignOrders
from delivery.core.application.use_cases.commands.move_couriers import MoveCouriers


app = Celery(__name__, broker=settings.redis_url, backend=settings.redis_url)


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Any, **_: Any) -> None:
    sender.add_periodic_task(
        settings.background_jobs_delays.assign_orders_delay_seconds,
        assign_orders,
        name="assign_orders_task",
    )
    sender.add_periodic_task(
        settings.background_jobs_delays.move_couriers_delay_seconds,
        move_couriers,
        name="move_orders_task",
    )


@shared_task
def assign_orders():
    assign_orders = AssignOrders()()
    asyncio.get_event_loop().run_until_complete(assign_orders)


@shared_task
def move_couriers():
    move_couriers = MoveCouriers()()
    asyncio.get_event_loop().run_until_complete(move_couriers)

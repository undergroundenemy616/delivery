from delivery.config.dependencies import get_container
from delivery.core.domain.services.find_courier_for_order import FindCourierForOrder
from delivery.utils.application_primitives import Command
from delivery.core.ports.uow_interface import UnitOfWork


class AssignOrders(Command):
    def __init__(self):
        self.uow = get_container().resolve(UnitOfWork)

    async def __call__(self):
        async with self.uow:
            orders = await self.uow.order.get_created_orders()
            if not orders:
                return

            order = orders[0]
            free_couriers = await self.uow.courier.get_free_couriers()
            if not free_couriers:
                return

            courier = FindCourierForOrder()(order=order, couriers=free_couriers)
            order.assign(courier)
            courier.set_busy()

            await self.uow.order.update_order(order_aggregate=order)
            await self.uow.courier.update_courier(courier_aggregate=courier)
            await self.uow.commit()

from delivery.utils.application_primitives import Command
from delivery.utils.uow.uow_interface import UnitOfWork


class MoveCouriers(Command):

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self):
        async with self.uow:
            orders = await self.uow.order.get_assigned_orders()
            if not orders:
                return

            for order in orders:
                courier = await self.uow.courier.get_courier_by_id(courier_id=order.courier_id)
                courier.move(order.location)
                if courier.location == order.location:
                    order.complete()
                    courier.set_free()

                await self.uow.order.update_order(order_aggregate=order)
                await self.uow.courier.update_courier(courier_aggregate=courier)
        await self.uow.commit()

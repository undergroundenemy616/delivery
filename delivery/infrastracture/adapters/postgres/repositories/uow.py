from delivery.infrastracture.adapters.postgres.repositories.courier_repository import CourierRepository
from delivery.infrastracture.adapters.postgres.repositories.order_repository import OrderRepository
from delivery.utils.uow.uow_interface import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    courier: CourierRepository
    order: OrderRepository

    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        self.courier = CourierRepository(self.session)
        self.order = OrderRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

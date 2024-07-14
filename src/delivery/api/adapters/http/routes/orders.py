import logging

from fastapi import APIRouter, Response
from starlette import status

from delivery.core.application.use_cases.commands.create_order import CreateOrder, CreateOrderDTO
from delivery.core.application.use_cases.queries.get_not_completed_orders import (
    GetNotCompletedOrders,
    GetNotCompletedOrdersOutputDTO,
)


router = APIRouter(
    prefix="/v1/orders",
    tags=["Orders"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_order(create_order_dto: CreateOrderDTO):
    create_order = CreateOrder()
    await create_order(create_order_dto=create_order_dto)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/active/", status_code=status.HTTP_200_OK, response_model=GetNotCompletedOrdersOutputDTO)
async def list_non_completed_orders():
    list_non_completed_orders = GetNotCompletedOrders()
    orders = await list_non_completed_orders()
    return orders

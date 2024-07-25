import logging

from fastapi import APIRouter, Body, Response, HTTPException
from starlette import status

from delivery.core.application.use_cases.commands.create_order import CreateOrder, CreateOrderDTO
from delivery.core.application.use_cases.queries.get_not_completed_orders import (
    GetNotCompletedOrders,
    GetNotCompletedOrdersOutputDTO,
)
from delivery.core.domain.model.courier_aggregate import CourierIsAlreadyBusyError
from delivery.core.domain.model.order_aggregate import OrderIsAlreadyAssignedError, OrderIsAlreadyCompletedError, OrderIsNotAssignedError

router = APIRouter(
    prefix="/v1/orders",
    tags=["Orders"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_order(create_order_dto: CreateOrderDTO | None = Body(default_factory=CreateOrderDTO)):
    create_order = CreateOrder()
    try:
        await create_order(create_order_dto=create_order_dto)
    except (
        CourierIsAlreadyBusyError,
        OrderIsAlreadyCompletedError,
        OrderIsAlreadyAssignedError,
        OrderIsNotAssignedError,
    ) as err:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/active/", status_code=status.HTTP_200_OK, response_model=list[GetNotCompletedOrdersOutputDTO])
async def list_non_completed_orders():
    list_non_completed_orders = GetNotCompletedOrders()
    orders = await list_non_completed_orders()
    return orders

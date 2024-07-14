import logging

from fastapi import APIRouter
from starlette import status

from delivery.core.application.use_cases.queries.get_busy_couriers import GetBusyCouriers, GetBusyCouriersOutputDTO


router = APIRouter(
    prefix="/v1/couriers",
    tags=["Couriers"],
)


logger = logging.getLogger(__name__)

#
# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_order(
#     uow: UOWDep,
#     create_order_dto: CreateOrderDTO
# ):
#     create_order = CreateOrder(uow=uow)
#     await create_order(create_order_dto=create_order_dto)
#     return Response(status_code=status.HTTP_201_CREATED)
#


@router.get("/", status_code=status.HTTP_200_OK, response_model=GetBusyCouriersOutputDTO)
async def list_couriers():
    list_busy_couriers = GetBusyCouriers()
    couriers = await list_busy_couriers()
    return couriers

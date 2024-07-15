from pydantic import BaseModel


class BackGroundJobsDelays(BaseModel):
    assign_orders_delay_seconds: int = 1
    move_couriers_delay_seconds: int = 1

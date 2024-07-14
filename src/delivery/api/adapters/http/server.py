from fastapi import FastAPI

from delivery.api.adapters.http.routes.couriers import router as couriers_router
from delivery.api.adapters.http.routes.orders import router as orders_router
from delivery.config.dependencies import get_container


def make_server() -> FastAPI:
    app = FastAPI(
        title="delivery",
        redoc_url=None,
    )
    get_container()
    app.include_router(orders_router)
    app.include_router(couriers_router)

    return app

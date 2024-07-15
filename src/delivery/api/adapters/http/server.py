from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from delivery.api.adapters.http.routes.couriers import router as couriers_router
from delivery.api.adapters.http.routes.orders import router as orders_router
from delivery.config.dependencies import get_container


def make_server() -> FastAPI:
    app = FastAPI(
        title="delivery",
        redoc_url=None,
    )
    get_container()
    app.include_router(orders_router, prefix="/api")
    app.include_router(couriers_router, prefix="/api")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://0.0.0.0:8086", "http://localhost:8086"],  # Разрешенные источники
        allow_credentials=True,
        allow_methods=["*"],  # Разрешенные методы (GET, POST и т.д.)
        allow_headers=["*"],  # Разрешенные заголовки (например, Authorization)
    )

    return app

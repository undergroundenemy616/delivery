import logging.config
import uvicorn


from delivery.api.adapters.http.server import make_server
from delivery.config import settings
from delivery.config import Stand


logging.config.dictConfig(settings.logging.as_dictconfig())
logger = logging.getLogger(__name__)


app = make_server()


@app.get("x", tags=["Monitoring"])
def ping_handler() -> dict:
    return {"status": "OK"}


def get_uvicorn_params():
    base = {"host": "::"}
    if settings.stand == Stand.local:
        return {**base, "port": 8082, "reload": True}
    return {**base, "port": 80}


def run_app():
    return uvicorn.run("main:app", **get_uvicorn_params(), log_config=settings.logging.as_dictconfig())


if __name__ == "__main__":
    run_app()

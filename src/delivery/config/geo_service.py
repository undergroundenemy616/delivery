from pydantic import BaseModel


class GeoServiceSettings(BaseModel):
    host: str = "localhost"
    port: int = 5004

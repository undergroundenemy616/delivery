from pydantic import BaseModel


class Address(BaseModel):
    country: str
    city: str
    street: str
    house: str
    apartment: str


class BasketConfirmedIntegrationEvent(BaseModel):
    basket_id: str
    address: Address

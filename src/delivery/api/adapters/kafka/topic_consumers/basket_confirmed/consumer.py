from faststream import FastStream
from faststream.kafka import KafkaBroker

from delivery.api.adapters.kafka.topic_consumers.basket_confirmed.event_schema import BasketConfirmedIntegrationEvent
from delivery.config import settings
from delivery.core.application.use_cases.commands.create_order import CreateOrder, CreateOrderDTO


broker = KafkaBroker(f"{settings.kafka.host_external}:{settings.kafka.port_external}")
basket_confirmed_consumer = FastStream(broker)


@basket_confirmed_consumer.broker.subscriber(settings.kafka.basket_confirmed_topic_name)
async def on_basket_confirmed(msg: BasketConfirmedIntegrationEvent):
    create_order_dto = CreateOrderDTO(basket_id=msg.basket_id, street=msg.address.street)
    create_order = CreateOrder()
    await create_order(create_order_dto=create_order_dto)

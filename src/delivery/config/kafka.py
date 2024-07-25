from pydantic import BaseModel


class KafkaSettings(BaseModel):
    host: str = "kafka"
    port: int = 29092

    host_external: str = "localhost"
    port_external: int = 9092

    basket_confirmed_topic_name: str = "basket.confirmed"
    order_status_changed_topic_name: str = "order.status.changed"

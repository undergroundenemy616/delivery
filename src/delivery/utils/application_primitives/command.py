import itertools
from abc import abstractmethod

from delivery.utils.ddd_primitives import Aggregate


class Command:

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    async def publish_domain_events(aggregates: list[Aggregate]):
        from delivery.core.application.domain_event_handlers import DOMAIN_EVENT_HANDLER_MAPPING
        domain_events = list(itertools.chain.from_iterable(aggregate.list_domain_events() for aggregate in aggregates))
        for aggregate in aggregates:
            aggregate.clear_domain_events()
        for domain_event in domain_events:
            event_handler = DOMAIN_EVENT_HANDLER_MAPPING.get(type(domain_event))
            await event_handler()(domain_event=domain_event)



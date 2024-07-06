from delivery.utils.ddd_primitives.aggregate import Aggregate


class AggregateMixin:
    def to_aggregate(self) -> Aggregate:
        raise NotImplementedError

from delivery.utils.ddd_primitives.entity import Entity


class EntityMixin:
    def to_entity(self) -> Entity:
        raise NotImplementedError

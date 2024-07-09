from abc import abstractmethod


class DomainService:

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

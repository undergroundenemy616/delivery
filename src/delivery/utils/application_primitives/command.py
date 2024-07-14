from abc import abstractmethod


class Command:

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

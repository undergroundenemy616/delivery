from abc import abstractmethod


class Query:

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

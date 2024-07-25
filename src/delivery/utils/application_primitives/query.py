from abc import abstractmethod


class Query:

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        raise NotImplementedError

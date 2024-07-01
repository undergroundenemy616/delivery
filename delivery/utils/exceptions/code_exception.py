import abc


class CodeExceptionError(abc.ABC, Exception):
    code: str

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

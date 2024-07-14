from enum import StrEnum, auto


class StorageTypes(StrEnum):
    postgres = auto()


class Stand(StrEnum):
    local = auto()
    testing = auto()
    prod = auto()

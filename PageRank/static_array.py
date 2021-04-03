from typing import Generic, TypeVar

T = TypeVar('T')


class Array(Generic[T]):
    value:T
    def __init__(self , length: int):
        self.__length = length
        self.__list = [0] * length

    def __len__(self):
        return self.__length

    def __getitem__(self, key: int) -> T:
        return self.__list[key]

    def __setitem__(self, key: int, value: T):
        self.__list[key] = value

    def __iter__(self):
        return self.__list.__iter__()

    def __str__(self):
        return str(self.__list)
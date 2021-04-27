from typing import Callable


class LogLog:
    def __init__(self, hash_function: Callable[..., str]):
        self.__hash_function = hash_function
        self.__max_zeroes = 0

    def process(self, value):
        result = self.__hash_function(value)
        trailing_zeroes = LogLog.__get_trailing_zeroes_count_hex(result)
        if trailing_zeroes > self.__max_zeroes:
            self.__max_zeroes = trailing_zeroes

    def get_result(self) -> int:
        return 2**self.__max_zeroes

    @staticmethod
    def __get_trailing_zeroes_count_hex(hex: str) -> int:
        position = len(hex) - 1
        counter = 0
        while True:
            if position == -1:
                return counter
            elif hex[position] == '0':
                counter += 4
                position -= 1
                continue
            elif hex[position] in {'2', '6', 'a', 'e'}:
                return counter + 1
            elif hex[position] in {'4', 'c'}:
                return counter + 2
            elif hex[position] in {'8'}:
                return counter + 3
            else:
                return counter

    # @staticmethod
    # def __get_trailing_zeroes_count_dec(number: int) -> int:
    #     counter = 0
    #     while number % 2 == 0:
    #         number = number // 2
    #         counter += 1
    #     return counter



from typing import TypeVar, Generic, Callable
from py_linq import Enumerable
import math

T = TypeVar('T')

def _sum_lists(a: list[int], b: list[int]) -> list[int]:
    return Enumerable(a).zip(Enumerable(b), lambda x, y: x + y).to_list()

def _or_lists(a: list[int], b: list[int]) -> list[int]:
    return Enumerable(a).zip(Enumerable(b), lambda x, y: _or(x, y)).to_list()

def _subtract_list(a: list[int], b: list[int]) -> list[int]:
    return Enumerable(a).zip(Enumerable(b), lambda x, y: x - y).to_list()

def _or(a: int, b: int):
    return a != 0 or b != 0

def _implication(a: int, b: int):
    return a == 0 or b != 0

class CountableBloomFilter(Generic[T]):
    def __init__(self, length: int, *args: Callable[[T], str]):
        if len(args) == 0:
            raise ValueError("Can't create countable bloom filter without hash functions")
        self.__hash_functions = args
        self.__bloom_filter = [0] * length
        self.__elements_count = 0

    def __hash_element(self, element: T) -> list[int]:
        return Enumerable(self.__hash_functions).select(
            lambda x: _string_to_char_list(x(element), len(self.__bloom_filter))).aggregate(lambda x, y: _or_lists(x, y))

    def add(self, element: T):
        self.__elements_count += 1
        self.__bloom_filter = _sum_lists(self.__bloom_filter, self.__hash_element(element))

    def remove(self, element: T):
        self.__elements_count -= 1
        self.__bloom_filter = _subtract_list(self.__bloom_filter, self.__hash_element(element))

    def contains(self, element: T) -> bool:
        return Enumerable(self.__hash_element(element)).zip(self.__bloom_filter, lambda x, y: (x, y)).all(lambda x: _implication(x[0], x[1]))

    def get_false_positive_probability(self):
        return (1 - math.exp(-len(self.__hash_functions) * self.__elements_count / len(self.__bloom_filter))) ** len(self.__hash_functions)

def _string_to_char_list(string: str, max_length: int):
    string_list = []
    string_list[0:max_length] = string # Supposed to convert string to the list of characters https://www.geeksforgeeks.org/python-splitting-string-to-list-of-characters/
    return string_list

# __hex_chars_dictionary = {'0': [0, 0, 0, 0], '1': [0, 0, 0, 1], '2': [0, 0, 1, 0], '3': [0, 0, 1, 1],
#                           '4': [0, 1, 0, 0], '5': [0, 1, 0, 1], '6': [0, 1, 1, 0], '7': [0, 1, 1, 1],
#                           '8': [1, 0, 0, 0], '9': [1, 0, 0, 1], 'A': [1, 0, 1, 0], 'B': [1, 0, 1, 1],
#                           'C': [1, 1, 0, 0], 'D': [1, 1, 0, 1], 'E': [1, 1, 1, 0], 'F': [1, 1, 1, 1]}
#
#
# def __hex_char_to_binary_list(hex_char: str) -> list[int]:
#     if len(hex_char) != 1:
#         raise ValueError()
#     return __hex_chars_dictionary[hex_char]
#
#
# def __hex_to_binary_list(hex_string: str, length: int) -> list[int]:
#     string_list = []
#     string_list[0:length] = hex_string # Supposed to convert string to the list of characters https://www.geeksforgeeks.org/python-splitting-string-to-list-of-characters/
#     return Enumerable(string_list).select(lambda x: __hex_char_to_binary_list(x)).aggregate(lambda x, y: x + y, [])



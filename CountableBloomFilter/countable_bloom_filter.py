from typing import TypeVar, Generic, Callable
# from py_linq import Enumerable
import math

T = TypeVar('T')

# def _sum_lists(a: list[int], b: list[int]) -> list[int]:
#     return Enumerable(a).zip(Enumerable(b), lambda x, y: x + y).to_list()

# def _or_lists(a: list[int], b: list[int]) -> list[int]:
#     return Enumerable(a).zip(Enumerable(b), lambda x, y: _or(x, y)).to_list()

# def _subtract_list(a: list[int], b: list[int]) -> list[int]:
#     return Enumerable(a).zip(Enumerable(b), lambda x, y: x - y).to_list()

# def _or(a: int, b: int):
#     return a != 0 or b != 0

# def _implication(a: int, b: int):
#     return a == 0 or b != 0

class CountableBloomFilter(Generic[T]):
    def __init__(self, length: int, *args: Callable[[T], int]):
        if len(args) == 0:
            raise ValueError("Can't create countable bloom filter without hash functions")
        self.__hash_functions = args
        self.__bloom_filter = [0] * length
        self.__elements_count = 0

    def __hash_element(self, element: T) -> set[int]:
        return set(map(lambda x: x(element) % len(self.__hash_functions), self.__hash_functions))

    def add(self, element: T):
        for i in self.__hash_element(element):
            self.__bloom_filter[i] += 1

    def remove(self, element: T):
        for i in self.__hash_element(element):
            self.__bloom_filter[i] -= 1

    def contains(self, element: T) -> bool:
        for i in self.__hash_element(element):
            if self.__bloom_filter[i] == 0:
                return False
        return True

    def get_false_positive_probability(self):
        return (1 - math.exp(-len(self.__hash_functions) * self.__elements_count / len(self.__bloom_filter))) ** len(self.__hash_functions)

def optimal_hash_functions_count(length: int, false_positive_probability: float, expected_elements_count: int) -> int:
    return round(math.log(2) * length / expected_elements_count)

# def _string_to_char_list(string: str, max_length: int):
#     string_list = []
#     string_list[0:max_length] = string # Supposed to convert string to the list of characters https://www.geeksforgeeks.org/python-splitting-string-to-list-of-characters/
#     return string_list

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



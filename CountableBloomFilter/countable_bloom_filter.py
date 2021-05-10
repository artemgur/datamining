from typing import TypeVar, Generic, Callable
import math

T = TypeVar('T')

class CountableBloomFilter(Generic[T]):
    def __init__(self, length: int, *args: Callable[[T], int]):
        if len(args) == 0:
            raise ValueError("Can't create countable bloom filter without hash functions")
        self.__hash_functions = args
        self.__bloom_filter = [0] * length
        self.__elements_count = 0

    def __hash_element(self, element: T) -> set[int]:
        return set(map(lambda x: x(element) % len(self.__bloom_filter), self.__hash_functions))

    def add(self, element: T) -> bool:
        contains_result = self.__contains(element)
        if contains_result[0]:
            return False
        element_hash = contains_result[1]
        self.__elements_count += 1
        for i in element_hash:
            self.__bloom_filter[i] += 1
        return True

    def remove(self, element: T) -> bool:
        contains_result = self.__contains(element)
        if contains_result[0]:
            return False
        element_hash = contains_result[1]
        self.__elements_count -= 1
        for i in element_hash:
            self.__bloom_filter[i] -= 1
        return True

    def __contains(self, element: T) -> (bool, set[int]):
        element_hash = self.__hash_element(element)
        for i in element_hash:
            if self.__bloom_filter[i] == 0:
                return False
        return True, element_hash

    def contains(self, element: T):
        return self.__contains(element)[0]

    def get_false_positive_probability(self):
        return (1 - math.exp(-len(self.__hash_functions) * self.__elements_count / len(self.__bloom_filter))) ** len(self.__hash_functions)

def get_optimal_hash_functions_count(length: int, expected_elements_count: int) -> int:
    return round(math.log(2) * length / expected_elements_count)

def get_optimal_length(expected_elements_count, false_positive_probability):
    return math.ceil(expected_elements_count * math.log(false_positive_probability) / (math.log(1 / 2 ** math.log(2))))

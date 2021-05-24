from typing import Iterable, TypeVar, Callable, Any
from collections import defaultdict
from bitmap import BitMap
from py_linq import Enumerable

T = TypeVar('T')


class Multistage:
    def __init__(self, support: int, baskets: Iterable, pass1_hash_function: Callable[[Any, Any], int], pass2_hash_function: Callable[[Any, Any], int], hash_buckets_count: int):
        self.__baskets_source = baskets
        self._support = support
        self.__baskets: list[[]] = []
        self._frequent_singletons = []
        self._pass1_hash_function = pass1_hash_function
        self._pass2_hash_function = pass2_hash_function
        self._hash_buckets_count = hash_buckets_count
        self.__launched = False
        self.__number_of_singletons = -1  # To adjust buckets count in future

    def __list_to_bitmap(self, l: list) -> BitMap:
        bitmap = BitMap(len(l))
        for i in range(0, len(l)):
            if l[i] >= self._support:
                bitmap.set(i)
        return bitmap

    def __hash1(self, pair: (Any, Any)):
        return self._pass1_hash_function(*pair) % self._hash_buckets_count

    def __hash2(self, pair: (Any, Any)):
        return self._pass2_hash_function(*pair) % self._hash_buckets_count

    def __pass1(self):
        singletons_count = defaultdict(int)
        pass1_hash_buckets = [0] * self._hash_buckets_count
        for basket in self.__baskets_source:
            self.__baskets.append(basket)
            for singleton in basket:
                singletons_count[singleton] += 1
            pairs = generate_pairs(basket)
            for pair in pairs:
                hash_function_result = self.__hash1(pair)
                pass1_hash_buckets[hash_function_result] += 1
        self.__pass1_bitmap = self.__list_to_bitmap(pass1_hash_buckets)
        self.__number_of_singletons = len(singletons_count.keys())
        self.__frequent_singletons = set(Enumerable(singletons_count.keys()).where(lambda key: singletons_count[key] >= self._support))

    def __pass2(self):
        pass2_hash_buckets = [0] * self._hash_buckets_count
        for basket in self.__baskets:
            for pair in generate_pairs(basket):
                if self.__is_pair_elements_frequent(pair) and self.__is_in_bucket1(pair):
                    pass2_hash_buckets[self.__hash2(pair)] += 1
        self.__pass2_bitmap = self.__list_to_bitmap(pass2_hash_buckets)
        
    def __is_in_bucket1(self, pair: (Any, Any)):
        return self.__pass1_bitmap.test(self.__hash1(pair))
    
    def __is_in_bucket2(self, pair: (Any, Any)):
        return self.__pass2_bitmap.test(self.__hash2(pair))
    
    def __is_pair_elements_frequent(self, pair: (Any, Any)):
        return set(pair).issubset(self.__frequent_singletons)

    def __get_frequent_doubletons(self):
        result = set()
        for basket in self.__baskets:
            for pair in generate_pairs(basket):
                if self.__is_pair_elements_frequent(pair) and self.__is_in_bucket1(pair) and self.__is_in_bucket2(pair):
                    result.add(pair)
        self.__frequent_doubletons = result
                
    def run(self) -> (set, set):
        if not self.__launched:
            self.__launched = True
            self.__pass1()
            self.__pass2()
            self.__get_frequent_doubletons()
        return self.__frequent_singletons, self.__frequent_doubletons

    def number_of_singletons(self):
        return self.__number_of_singletons

    def number_of_baskets(self):
        return len(self.__baskets)


def generate_pairs(source: list[T]) -> list[(T, T)]:
    result = []
    for i in range(len(source)):
        for j in range(i + 1, len(source)):
            result.append((source[i], source[j]))
    return result


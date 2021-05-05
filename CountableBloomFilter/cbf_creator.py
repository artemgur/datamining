import hasher
import countable_bloom_filter
import math


def create(length: int, hash_functions_count: int) -> countable_bloom_filter.CountableBloomFilter:
    return countable_bloom_filter.CountableBloomFilter(length, *list(map(lambda x: hasher.Hasher().hash, [None] * hash_functions_count)))

def create_optimal(false_positive_probability: float, expected_elements_count: int) -> countable_bloom_filter.CountableBloomFilter:
    length = math.ceil(expected_elements_count * math.log(false_positive_probability) / (math.log(1 / 2 ** math.log(2))))
    return create(length, countable_bloom_filter.optimal_hash_functions_count(length, false_positive_probability, expected_elements_count))

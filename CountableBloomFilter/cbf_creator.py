import hasher
import countable_bloom_filter


def create(length: int, hash_functions_count: int) -> countable_bloom_filter.CountableBloomFilter:
    return countable_bloom_filter.CountableBloomFilter(length, *list(map(lambda x: hasher.Hasher().hash, [None] * hash_functions_count)))

def create_optimal(false_positive_probability: float, expected_elements_count: int) -> countable_bloom_filter.CountableBloomFilter:
    length = countable_bloom_filter.get_optimal_length(expected_elements_count, false_positive_probability)
    return create(length, countable_bloom_filter.get_optimal_hash_functions_count(length, expected_elements_count))



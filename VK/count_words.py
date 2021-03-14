import get_text
from collections import defaultdict
import regex


def count_words(post_number: int):
    result = defaultdict(int)
    for i in range(post_number):
        text = regex.sub(r'[^\p{L}\s-]+', '', get_text.get_text(i)).lower().split()
        for word in text:
            result[word] += 1
        result.pop('-', None)
    return result

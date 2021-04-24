import requests
import random
import time

numbers_count = 100
__min_number = 0
__max_number = 1000
__time_between_numbers = 0.2


def generate():
    for i in range(numbers_count):
        requests.post('localhost:8000', data=random.randint(__min_number, __max_number))
        time.sleep(__time_between_numbers)